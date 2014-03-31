import normalize

IMG1 = [
    [1,1,0,1,1],
    [1,1,0,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,1,1,0]
]

IMG2 = [
    [1,1,0,1,1],
    [1,0,0,1,1],
    [1,0,1,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1]
]

IMG3 = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,1,0,0],
    [0,0,0,0,0],
    [0,1,1,0,0]
]

def test_acute_angles():
    assert normalize.is_acute_angle(IMG1, 2, 2)
    assert not normalize.is_acute_angle(IMG2, 2, 2)

def test_get_neighbors():
    neighbors1 = [1, 1, 1, 1, 1, 1, 0, 1]
    neighbors2 = [1, 1, 1, 1, 0, 0, 0, 1]
    assert normalize.get_neighbors_1(IMG1, 2, 2) == neighbors1
    assert normalize.get_neighbors_1(IMG2, 2, 2) == neighbors2

def test_connectivity():
    assert normalize.connectivity(IMG1, 2, 2) == 2
    assert normalize.connectivity(IMG2, 2, 2) == 2
    assert normalize.connectivity(IMG3, 2, 2) == 0

def test_num_black_neighbors():
    assert normalize.num_black_neighbors(IMG1, 2, 2) == 7
    assert normalize.num_black_neighbors(IMG2, 2, 2) == 5
    assert normalize.num_black_neighbors(IMG3, 2, 2) == 0

def test_is_spurious():
    assert normalize.is_spurious_projection(IMG3, 2, 2)
    assert not normalize.is_spurious_projection(IMG1, 2, 2)

def test_smooth_and_emphasize():
    normalize.smooth_and_emphasize_angles(IMG1)
    normalize.smooth_and_emphasize_angles(IMG3)
    print IMG3
    assert IMG1[2][2] == 0
    assert IMG3[2][2] == 0
