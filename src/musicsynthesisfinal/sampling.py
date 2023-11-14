import math
from typing import Any, List, Optional, Union
import torch


def build_mask(len_probs: int, tokens):
    """            
    Generates a mask from the given indices of tokens.

    # Parameters

        len_probs (`int`):
            The length of the next token probability distribution.
        tokens (`array_like`):
            Indices of tokens need to be masked.

    # Returns

        mask (`ndarray`): 
            A boolean array with the length of `len_probs` where indices given in `tokens` are `True`.

    # Examples

        >>> from samplings import build_mask
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> tokens = [0, 3]
        >>> build_mask(len_probs=len(probs), tokens=tokens)
        [ True False False  True]
    """

    # Initialising the mask
    mask = torch.zeros(len_probs).type(torch.bool)

    # Set masked tokens
    if len(tokens) != 0:
        mask[tokens] = True

    return mask


def random_sampling(probs):
    """            
    Selects a random index from the given probability distribution.

    # Parameters

        probs (`array_like`):
            The probability distribution.
        seed (`int`, *optional*, defaults to `None`):
            Seed for RandomState. Must be convertible to 32-bit unsigned integers.

    # Returns

        index (`int`): 
            The randomly sampled index of the next token from `probs`.

    # Tips

        For reproducibility, you can set `seed` to an integer.

    # Examples

        >>> from samplings import random_sampling
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> random_sampling(probs=probs, seed=0)
        2
    """

    # return np.random.choice(range(len(probs)), p=probs)
    dist = probs.clone()
    dist_cum = torch.cumsum(dist, 0)
    return torch.searchsorted(
        dist_cum, torch.rand(size=(1, )))[0]


def top_p_sampling(probs,
                   top_p: float,
                   return_probs: bool = False):
    """            
    Also known as nucleus sampling, which shortlists the top tokens whose sum of likelihoods does not exceed a certain value. 

    # Parameters

        probs (`array_like`):
            The probability distribution.
        top_p (`float`):
            A positive decimal which not greater than 1.
            Only the most possible tokens with probabilities that add up to 
            `top_p` or higher are kept for generation.
        seed (`int`, *optional*, defaults to `None`):
            Seed for RandomState. Must be convertible to 32-bit unsigned integers.
        return_probs (`bool`, *optional*, defaults to `False`):
            Whether or not to return the modified probability distribution. 
            If set to `False`, return the randomly sampled index.

    # Returns

        index (`int`)
            The randomly sampled index of the next token from modified `probs` (when `return_probs` is `False`).
        probs (`ndarray`):
            The modified probability distribution (when `return_probs` is `True`).

    # Tips

        For reproducibility, you can set `seed` to an integer.\n
        When used with `return_probs=True`, you can get the modified probability distribution.\n
        Then, you can make further manipulations based on this probability distribution.\n

    # Examples

        >>> from samplings import top_p_sampling
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> top_p_sampling(probs=probs, 
                           top_p=0.5,
                           return_probs=True)
        [0.         0.         0.42857143 0.57142857]
        >>> top_p_sampling(probs=probs, 
                           top_p=0.7,
                           return_probs=True)
        [0.         0.22222222 0.33333333 0.44444444]

    # References

        - Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi: 
        ["The Curious Case of Neural Text Degeneration"](https://arxiv.org/pdf/1904.09751.pdf). ICLR 2020
    """

    if 0 < top_p and top_p < 1:
        # Sort probability distribution
        sorted_tokens = torch.argsort(probs, descending=True)
        sorted_probs = torch.log(torch.sort(probs, descending=True)[0])
        cumulative_probs = torch.logcumsumexp(sorted_probs, 0)
        sorted_tokens_to_remove = cumulative_probs > math.log(top_p)

        # Logical right shift
        sorted_tokens_to_remove = torch.roll(sorted_tokens_to_remove, 1)
        sorted_tokens_to_remove[0] = False

        # Remove tokens with small probabilities
        tokens_to_remove = sorted_tokens[sorted_tokens_to_remove]
        mask = build_mask(len(probs), tokens_to_remove)
        # probs = np.ma.array(probs, mask=~mask)
        probs[mask] -= probs[mask]
        # probs = torch.tensor(probs)
        probs /= probs.sum()

    # Return probability distribution
    if return_probs:
        return probs

    # Return index
    else:
        return random_sampling(probs)


def temperature_sampling(probs,
                         temperature: float,
                         weights=None,
                         tempered_tokens: Optional[List[int]] = None,
                         return_probs: bool = False) -> Union[torch.Tensor, int]:
    """            
    Lower temperatures (< 1) make the model increasingly confident in its top choices and vice versa.

    If you want to use penalized sampling, please set `weights` to an array with the same length of `probs`.

    If only some of the tokens' probabilities are intended to be changed, you can specify their indices by setting `tempered_tokens`.

    # Parameters

        probs (`array_like`):
            The probability distribution.
        temperature (`float`):
            A non-negative number which used to module the sharpness of the probability distribution.
        weights (`array_like`, *optional*, defaults to `1`):
            An array of probability weights for temperature sampling with the same length of `probs`.
        tempered_tokens (`array_like`, *optional*, defaults to `[]`):
            A list of indices of tokens need to be tempered, the rest tokens' probabilities will keep intact.
        seed (`int`, *optional*, defaults to `None`):
            Seed for RandomState. Must be convertible to 32-bit unsigned integers.
        return_probs (`bool`, *optional*, defaults to `False`):
            Whether or not to return the modified probability distribution. 
            If set to `False`, return the randomly sampled index.

    # Returns

        index (`int`):
            The randomly sampled index of the next token from modified `probs` (when `return_probs` is `False`).
        probs (`ndarray`):
            The modified probability distribution (when `return_probs` is `True`).

    # Tips

        For reproducibility, you can set `seed` to an integer.\n
        When used with `return_probs=True`, you can get the modified probability distribution.\n
        Then, you can make further manipulations based on this probability distribution.\n

    # Examples

        >>> from samplings import temperature_sampling
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> weights = [1.2, 1.2, 1, 1]
        >>> tempered_tokens = [0, 1]
        >>> temperature_sampling(probs=probs, 
                                 temperature=0.5,
                                 return_probs=True)
        [0.03333333 0.13333333 0.3        0.53333333]
        >>> temperature_sampling(probs=probs, 
                                 temperature=0.5,
                                 weights=weights,
                                 return_probs=True)
        [0.01447698 0.07640994 0.32728071 0.58183237]
        >>> temperature_sampling(probs=probs, 
                                 temperature=0.5,
                                 tempered_tokens=tempered_tokens,
                                 return_probs=True)
        [0.06 0.24 0.3  0.4 ]

    # References

        - David H. Ackley, Geoffrey E. Hinton, Terrence J. Sejnowski: 
        ["A Learning Algorithm for Boltzmann Machines"](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1207/s15516709cog0901_7). Cogn. Sci. 9(1): 147-169 (1985)

        - Nitish Shirish Keskar, Bryan McCann, Lav R. Varshney, Caiming Xiong, Richard Socher: 
        ["CTRL: A Conditional Transformer Language Model for Controllable Generation"](https://arxiv.org/pdf/1909.05858.pdf). CoRR abs/1909.05858 (2019)
    """
    weights = torch.tensor(1)
    tempered_tokens: List[int] = []

    if temperature != 1:
        # Mask modified tokens
        if len(tempered_tokens) == 0:
            # tempered_tokens = list(range(len(probs)))
            tempered_tokens = torch.jit.annotate(
                List[int], list(range(len(probs))))

        modified_mask = build_mask(len(probs), torch.tensor(tempered_tokens))
        modified_sum = torch.dot(probs, modified_mask)

        # Divide log probability by the temperature before softmax
        probs = torch.where(modified_mask, probs/modified_sum, probs)
        probs = torch.where(modified_mask, torch.log(probs) *
                            torch.tensor(weights)/temperature, probs)
        probs = torch.where(modified_mask, modified_sum*torch.exp(probs) /
                            torch.sum(torch.where(modified_mask, torch.exp(probs), 0)), probs)

    # Return probability distribution
    if return_probs:
        return probs

    # Return index
    else:
        return random_sampling(probs)
