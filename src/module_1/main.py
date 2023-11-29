import math


def calc_h_x(*px: float) -> float:
    results = [x * math.log2(x) for x in px if x != 0]
    return -sum(results)


def calc_h_k(*pk: float) -> float:
    results = [k * math.log2(k) for k in pk if k != 0]
    return -sum(results)


def calc_h_y(*py: float) -> float:
    results = [y * math.log2(y) for y in py if y != 0]
    return -sum(results)


def main() -> None:
    p_x1, p_x2, p_x3 = 0.3, 0.41, 0.29
    p_k1, p_k2, p_k3 = 0.17, 0.8, 0.03
    p_y1, p_y2, p_y3 = 0.29529, 0.3187, 0.386

    h_x = calc_h_x(p_x1, p_x2, p_x3)
    h_k = calc_h_k(p_k1, p_k2, p_k3)
    h_y = calc_h_y(p_y1, p_y2, p_y3)
    print(f"Entropy H(X) = {h_x:.4f}")
    print(f"Entropy H(K) = {h_k:.4f}")
    print(f"Entropy H(Y) = {h_y:.4f}")

    print(f"Entropy H(K|Y) = {h_k + h_x - h_y:.4f}")


if __name__ == "__main__":
    main()
