import copy

import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
from attacks.attackbox.attack_base_different_input import Attack_different_input



class PGD(Attack_different_input):
    """
    PGD evasion attack based on gradient of TWO Models synchronically:
    The PGD attack can only take one input sample each time during the attacking process
        - PGD in the paper 'Towards Deep Learning Models Resistant to Adversarial Attacks'
        - [https://arxiv.org/abs/1706.06083]

    Distance Measure : Linf

    Arguments:
        model_1 (nn.Module): model_1 to attack. (default as Malconv)
        model_2: model_2 to attack. (default as DNN from FireEye)
        index_to_perturb: a list of index can be added noise;
            - Default as first part of DOS header [2,0x3c] ([2,60]), except the first Magic number "MZ"
        alpha (float): maximum perturbation. (DEFALUT: 0.3)
        eps (float): perturbation step size. (DEFALUT: 0.07)
        random_init:
            - True --> add random (Gaussim) noise to input x at first place to improve the performance
            - False --> no changes to input x
        pert_init_with_benign:
            - True --> initiate perturbations by adding bytes from benign files (randomly select) to the position of index_to_perturb
            - False --> random initiate values in position of index_to_perturb to value range in [0,256]
        w_1: weight to control the weight of model_1 when compute the loss function
        w_2: weight to control the weight of model_2 when compute the loss function

    Shape:
        - inputs: `(N, W)` where `N = number of batches`,  `W = width`. N has to be 1 !!
        - labels: `(N)` where `N = number of batches`, and each value is the corresponding label
        - output: :math:`(N, W)`.

    Examples:
        > attack = attackbox.PGD(model_1,model_2,eps=0.007,index_to_perturb=list)
        > adv_Xs = attack(inputs, labels)

    return:
        - if one target model: prediction scores, label of adversarial malware, size of perturbation (i.e., length of pert)
        - if two target models: (prediction_scores_1, adv_y_1), (prediction_scores_2, adv_y_2),size of perturbation (i.e., length of pert)

    """

    def __init__(self,
                 model_1=None,
                 model_2=None,
                 eps: float = 0.3,
                 alpha: float = 0.07,
                 w_1: float = 0.5,
                 w_2: float = 0.5,
                 iter_steps = 50,
                 index_to_perturb: list = None, # can also obtain in perturbation step
                 random_init: bool = False,
                 pert_init_with_benign: bool = True,
                 width = 320,
                 height = 320):

        ## 继承父类Attack的参数
        Attack_different_input.__init__(self,model_1=model_1,
                                        model_2=model_2,
                                        width= width,
                                        height= height)

        if not index_to_perturb or len(index_to_perturb)==0:
            index_to_perturb = [i for i in range(2, 0x3c)] ## partial dos length=58 ( magic numbers in DOS header "MZ"[0x00-0x02] and [0x3c-0x40] can't be modified)
            # print("Initiate crafting process with partial DOS header...")

        self.w_1, self.w_2 = w_1, w_2
        self.eps = eps
        self.alpha = alpha
        self.iter_steps = iter_steps
        self.index_to_perturb = index_to_perturb
        self.random_init = random_init
        self.pert_init_with_benign = pert_init_with_benign
        self.attack = 'PGD'
        self.width = width
        self.height = height


    def perturbation(self,
                     inputs: list = None,
                     index_to_perturb: list = None,
                     num_evasion_by_benign_content: int = 0,
                     num_index_change_in_total_group: list = [],
                     num_index_change_by_gradient_group: list = []):
        """
        inputs: the initiated inputs (with 0 initiated in perturb_index) after DOS_Extension/Content_Shift attacks
        the length of inputs should larger than original input sample

        num_evasion_w_benign_content: number of evasion times just with benign content or random bytes
        num_index_change_in_total_group: list append all num_index_change_in_total for each input malware
        num_index_change_by_gradient_group: list append with all num_byte_change_by_gradient for each input malware
        """

        ## get index_to_perturb, if exist, assign it to the global variable,
        ## otherwise no attack (i.e. this situation happenes when slack attack cannot find slack space)
        if len(index_to_perturb) > 0:
            self.index_to_perturb = index_to_perturb
        elif len(index_to_perturb) == 0:
            ## 1) no perturbatoin space found  --> return results based on original inputs
            ## 2) happens when the found indexes (e.g. [143432343,145645647]) are larger than the input size (102400),
            ## therefore, even though index_to_perturb exist, but it's still empty consider the input size
            self.index_to_perturb = index_to_perturb
            print('no available index found for perturb given the current input size')

            if self.model_2:
                (adv_x_preds_1, adv_y_1), (adv_x_preds_2, adv_y_2) = \
                    self._get_print_return_results(inputs, self.model_1, self.model_2, test_x_init=True)
                pert_size = len(self.index_to_perturb)
                return (adv_x_preds_1, adv_y_1), (adv_x_preds_2, adv_y_2), pert_size, num_evasion_by_benign_content, \
                       num_index_change_in_total_group, num_index_change_by_gradient_group
            else:
                adv_x_preds_1, adv_y_1 = self._get_print_return_results(inputs, self.model_1)
                pert_size = len(self.index_to_perturb)
                return adv_x_preds_1, adv_y_1, pert_size, num_evasion_by_benign_content, \
                       num_index_change_in_total_group, num_index_change_by_gradient_group

        # initiate input with benign content or random perturbations
        if self.pert_init_with_benign:
            benign_contents = self.get_section_content_from_folder(num_sections=100, target_section='.text')
        else:
            benign_contents = None

        ## get initiated adv_x with benign content or random bytes;
        ## and get perturbations (either benign contents or random values)
        adv_x_init,pert_init = self.apply_manipulations(inputs,
                                                        self.index_to_perturb,
                                                        self.pert_init_with_benign,
                                                        benign_contents=benign_contents)

        ## ------------------- print results for initiated x before attack and ternimate if needed -----------------------------
        ## test the initiated x that either with random value or benign content in the index_to_perturb
        (adv_x_preds_1,adv_y_1),(adv_x_preds_2,adv_y_2) = self._get_print_return_results(adv_x_init,
                                                                                         self.model_1,
                                                                                         self.model_2,
                                                                                         test_x_init=True)

        ## terminate when label already changed to benign (label=0)
        if adv_y_1 == 0 and adv_y_2 == 0:
            num_evasion_by_benign_content += 1
            return (adv_x_preds_1,adv_y_1),(adv_x_preds_2,adv_y_2),len(pert_init),num_evasion_by_benign_content, \
                   num_index_change_in_total_group, num_index_change_by_gradient_group

        ## else --> start adversarial evasion attacks
        ## update values in index_to_perturb with optimized values
        print('\n','-'*50)
        print(f'starting {self.attack} based adversarial evasion attack...')

        ## add dim at axis=0
        adv_x = torch.tensor(np.array(adv_x_init)[np.newaxis,:],device=self.device)

        ## ------------- apply gaussian noise (or others) on input before backward, which can improve the performance ----------------
        ## https://www.cnblogs.com/tangweijqxx/p/10615950.html
        # if self.random_init:
        #     x_adv = x_adv + torch.Tensor(np.random.uniform(-self.eps, self.eps, x_adv.shape)).\
        #         type_as(x_adv).to(self.device)

        ## forward process
        for i in range(self.iter_steps):
            print(f'{i} iteration for PGD...')

            adv_x = Variable(adv_x.float(), requires_grad=True).to(self.device)
            preds_1, embed_x_1 = self._forward(adv_x, self.model_1) # embed_x: float
            loss_1 = self.targeted* self.loss(preds_1, self.targeted_label)

            ## against 1 or 2 models
            if not self.model_2:
                loss = loss_1
            else:
                ## image: reshape to image format, and normalzied to [0,1]
                adv_x_2 = torch.reshape(adv_x, (1, 1, self.height, self.width)) / 255
                preds_2, embed_x_2 = self._forward(adv_x_2, self.model_2,model_type='image')
                loss_2 = self.targeted * self.loss(preds_2, self.targeted_label)
                loss = self.w_1 * loss_1 + self.w_2 * loss_2

            ## get the un-perturbed x. i.e. x before adding perturbation
            if i == 0:
                embed_x_init_1 = embed_x_1
                if self.model_2:
                    x_init_2 = adv_x_2

            ## zero_grad before backward, otherwise it will accumulate gradients in mini-batches
            self.model_1.zero_grad()
            if self.model_2:
                self.model_2.zero_grad()
            loss.backward(retain_graph=True)

            ## get sign and perturbation
            grad_sign_for_perturb_index_1 = self._get_grad_sign(embed_x_1,self.index_to_perturb)

            ## get adv_x by applied with adversarial evasion attack perturbations
            ## by add pert on adv_x initiated with benign contents or random bytes
            ## model 1: byte based
            adv_x1 = self._get_advX_for_PGD(x=adv_x_init,
                                            embed_x_init=embed_x_init_1,
                                            embed_x_adv=embed_x_1,
                                            sign=grad_sign_for_perturb_index_1,
                                            eps=self.eps,
                                            alpha=self.alpha,
                                            embed_matrix=self.embed_matrix_1,
                                            index_to_perturb=self.index_to_perturb)

            ## obtain final pertbation based on the either one model or two models
            ## one model: simple output pert = eps * sign
            ## two models: 1) if sign1=sign2 --> ... 2) else --> ...
            if self.model_2:
                ## model 2: image based
                grad_sign_for_perturb_2 = torch.autograd.grad(loss, adv_x_2,retain_graph=False, create_graph=False)[0].sign()

                ## get adv_x by applied with PGD based perturbations
                ## by add pert on adv_x initiated with benign contents or random bytes
                adv_x2 = self._get_advImage_for_PGD(x=x_init_2,
                                                x_adv=adv_x_2,
                                                sign=grad_sign_for_perturb_2,
                                                eps=self.eps,
                                                alpha=self.alpha,
                                                index_to_perturb=self.index_to_perturb)

                ## get final adv_x based on two adv_x from two models
                adv_x,num_index_change_in_total,num_index_change_by_gradient = \
                    self._final_adv_x_selection(x=adv_x_init,
                                                adv_x1=adv_x1,
                                                adv_x2=adv_x2,
                                                verbose=True,
                                                index_to_perturb=self.index_to_perturb)
                ## to tensor and add dim
                adv_x = torch.tensor(np.array(adv_x)[np.newaxis, :], device=self.device)
            else:
                ## only one model need to consider
                adv_x = adv_x1
                num_index_change_in_total = len(self.index_to_perturb)
                num_index_change_by_gradient = 0  # need to re-modify later, assign 0 for now
                ## to tensor and add dim
                adv_x = torch.tensor(np.array(adv_x)[np.newaxis, :], device=self.device)

            ## append num_index_change to list for records
            num_index_change_in_total_group.append(num_index_change_in_total)
            num_index_change_by_gradient_group.append(num_index_change_by_gradient)

        ## ------------------- print and get results for adv_x after PGD attack -----------------------------
        ## get prediction for produced adversarial example adv_x after PGD,
        ## print and return results (prediction score, prediction label, size of perturbation)
        if self.model_2:
            (adv_x_preds_1,adv_y_1),(adv_x_preds_2,adv_y_2) = \
                self._get_print_return_results(adv_x,self.model_1,self.model_2,test_x_init=False)
            pert_size = len(self.index_to_perturb)
            return (adv_x_preds_1,adv_y_1),(adv_x_preds_2,adv_y_2),pert_size,num_evasion_by_benign_content, \
                   num_index_change_in_total_group, num_index_change_by_gradient_group
        else:
            adv_x_preds_1, adv_y_1 = self._get_print_return_results(adv_x,self.model_1)
            pert_size = len(self.index_to_perturb)
            return adv_x_preds_1, adv_y_1,pert_size,num_evasion_by_benign_content, \
                   num_index_change_in_total_group, num_index_change_by_gradient_group







