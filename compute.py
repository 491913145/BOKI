# coding=gbk
import numpy as np


def convolution(x, kernel, stride, axes=((0, 2, 3), (1, 4, 5))):
    """
    ��άƽ���ϵľ����paddingΪVALID
    :param x: �����������������һ����ά����
    :param kernel: ����˲�����Ϊһ����ά����
    :param stride: ������Ϣ��һ��������
    :return: ���֮��ľ�����Ϣ
    """
    assert len(x.shape) == 4
    assert len(kernel.shape) == 4
    assert type(stride) is int
    n, c, h, w = x.shape
    i, o, k_h, k_w = kernel.shape
    assert (h - k_h) % stride == 0 and (w - k_w) % stride == 0
    x = split_by_strides(x, k_h, k_w, stride)
    # result = np.tensordot(kernel, x, axes=axes).transpose((1, 0, 2, 3))
    result = np.einsum('ijkl,nimukl->njmu', kernel, x, optimize=True)
    return result


def padding_zeros(x, left_right, top_bottom):
    """
    �Ծ������Χ�����0�Ĳ�����
    :param x: һ����ά����
    :param left_right: һ������Ϊ2�����飬�ֱ��ʾ�����Ҳ���Ҫ���0�Ĳ���
    :param top_bottom: һ������Ϊ2�����飬�ֱ��ʾ�ϲ���²���Ҫ���0�Ĳ���
    :return: �֮��ľ���
    """

    assert len(x.shape) == 2
    assert len(left_right) == 2 and len(top_bottom) == 2
    new_x = np.zeros([top_bottom[0] + top_bottom[1] + x.shape[0], left_right[0] + left_right[1] + x.shape[1]])
    new_x[top_bottom[0]: top_bottom[0] + x.shape[0], left_right[0]: left_right[0] + x.shape[1]] = x
    return new_x


def insert_zeros(x, stride):
    """
    �ھ����ÿ��������Ԫ��֮�����һ����Ŀ��0
    :param x: һ����ά����
    :param stride: һ���Ǹ���
    :return: ����0֮��ľ���
    """
    assert len(x.shape) == 4
    assert type(stride) is int and stride >= 0
    n, c, h, w = x.shape
    new_x = np.zeros([n, c, (h - 1) * stride + h, (w - 1) * stride + w])

    for i in range(h):
        for j in range(w):
            new_x[:, :, i * (stride + 1), j * (stride + 1)] = x[:, :, i, j]

    return new_x


def rotate_180_degree(x, axes=(2, 3)):
    """
    ��������ת180�㣬��һ����Ҫ����Ծ���˶��ԡ�
    :param x: ��Ҫ����ת�ľ���
    :return: ��ת֮��ľ���
    """

    # assert len(x.shape) == 4
    return np.rot90(np.rot90(x, axes=axes), axes=axes)


def split_by_strides(x, kh, kw, s):
    N, C, H, W = x.shape
    oh = (H - kh) // s + 1
    ow = (W - kw) // s + 1
    strides = (*x.strides[:-2], x.strides[-2] * s, x.strides[-1] * s, *x.strides[-2:])
    return np.lib.stride_tricks.as_strided(x, shape=(N, C, oh, ow, kh, kw), strides=strides)


def accuracy(y, y_pred, axis=1):
    y_pred = np.argmax(y_pred, axis=axis)
    y = np.argmax(y, axis=axis)
    correct_prediction = y_pred == y
    return np.mean(correct_prediction)


def to_categorical(y, classes):
    diag = np.diag(np.ones(classes))
    return diag[y]


def shuffle(x, y):
    state = np.random.get_state()
    np.random.shuffle(x)
    np.random.set_state(state)
    np.random.shuffle(y)
    return x, y
