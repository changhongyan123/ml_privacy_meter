import torch
import numpy as np


def get_signal_on_argumented_data(model_pm, data, targets, method=None):
    if method is None:
        return model_pm.get_loss(data, targets)
    elif method == "argumented":
        reflect = True
        shift = 0
        stride = 1

        outs = []
        for aug in [data, data.flip(dims=[3])][: reflect + 1]:
            aug_pad = torch.nn.functional.pad(aug, [shift] * 4, mode="reflect")
            for dx in range(0, 2 * shift + 1, stride):
                for dy in range(0, 2 * shift + 1, stride):
                    this_x = aug_pad[:, :, dx : dx + 32, dy : dy + 32]
                    logits = model_pm.get_loss(this_x, targets)
                    outs.append(logits)
        return np.transpose(np.array(outs), (1,0)) # (batch size, number of aug)

    else:
        raise NotImplementedError