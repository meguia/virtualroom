from functools import reduce 

def validate_room_schema(desc = {}):
    """
    Raises an exception if the room schema used for input is badly formatted 
    """
    expected_keys = [
                    'name', 
                    'dimensions', 
                    'wall_thickness', 
                    ]
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for room dictionary keys. '
                    'Expected keys: '
                    '\'name\', '
                    '\'dimensions\', '
                    '\'wall_thickness\', '
                    )
        raise KeyError(error_msg) 

    dimensions_desc = desc['dimensions']
    expected_keys = [
                    'depth', 
                    'width', 
                    'height'
                    ]
    keys_status = [key in dimensions_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for dimensions dictionary keys. '
                    'Expected keys: \'depth\', \'width\', \'height\''
                    )
        raise KeyError(error_msg)

def validate_door_schema(desc = {}):
    """
    Raises an exception if the door schema used for input is badly formatted 
    """
    expected_keys = [
                    'wall_index',
                    'position',
                    'width',
                    'height',
                    'frame',
                    ]
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for door dictionary keys. '
                    'Expected keys: '
                    '\'wall_index\' '
                    '\'position\' '
                    '\'width\' '
                    '\'height\' '
                    '\'frame\''
                    )
        raise KeyError(error_msg) 

def validate_spot_schema(desc = {}):
    """
    Raises an exception if the spot schema used for input is badly formatted 
    """
    expected_keys = [
                    'name',
                    'energy',
                    'size',
                    'blend',
                    'position', 
                    'rotation'
                    ]
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for spot dictionary keys. '
                    'Expected keys: '
                    '\'name\', '
                    '\'energy\', '
                    '\'size\', '
                    '\'blend\', '
                    '\'position\', '
                    '\'rotation\''
                    )
        raise KeyError(error_msg) 

    position_desc = desc['position']
    expected_keys = ['x', 'y', 'z']
    keys_status = [key in position_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for spot position dictionary keys. '
                    'Expected keys: \'x\', \'y\', \'z\''
                    )
        raise KeyError(error_msg)

    rotation_desc = desc['rotation']
    expected_keys = ['x', 'y', 'z']
    keys_status = [key in rotation_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for spot rotation dictionary keys. '
                    'Expected keys: \'x\', \'y\', \'z\''
                    )
        raise KeyError(error_msg)

def validate_speaker_schema(desc = {}):
    """
    Raises an exception if the speaker schema used for input is badly formatted 
    """
    expected_keys = ['position', 'rotation', '3d_model']
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for speaker dictionary keys. '
                    'Expected keys: '
                    '\'position\', '
                    '\'rotation\', '
                    '\'3d_model\', '
                    )
        raise KeyError(error_msg) 

    position_desc = desc['position']
    expected_keys = ['x', 'y', 'z']
    keys_status = [key in position_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for speaker position dictionary keys. '
                    'Expected keys: \'x\', \'y\', \'z\''
                    )
        raise KeyError(error_msg)

def validate_frame_schema(desc = {}):
    """
    Raises an exception if the frame schema used for input is badly formatted 
    """
    expected_keys = [
                    'width', 
                    'thickness'
                    ]
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for frame dictionary keys. '
                    'Expected keys: '
                    '\'width\', '
                    '\'thickness\''
                    )
        raise KeyError(error_msg) 

def validate_base_schema(desc = {}):
    """
    Raises an exception if the base schema used for input is badly formatted 
    """
    expected_keys = [
                    'height', 
                    'thickness'
                    ]
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for base dictionary keys. '
                    'Expected keys: '
                    '\'height\', '
                    '\'thickness\''
                    )
        raise KeyError(error_msg) 

def validate_camera_schema(desc = {}):
    """
    Raises an exception if the camera schema used for input is badly formatted 
    """
    expected_keys = ['position', 'rotation']
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for camera dictionary keys. '
                    'Expected keys: \'position\', \'rotation\''
                    )
        raise KeyError(error_msg) 

    position_desc = desc['position']
    expected_keys = ['x', 'y', 'z']
    keys_status = [key in position_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for camera position dictionary keys. '
                    'Expected keys: \'x\', \'y\', \'z\''
                    )
        raise KeyError(error_msg)

def validate_tube_schema(desc = {}):
    """
    Raises an exception if the tube schema used for input is badly formatted 
    """
    expected_keys = [
                    'object', 
                    'color',
                    'intensity', 
                    'mount', 
                    ]
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for tube dictionary keys. '
                    'Expected keys: '
                    '\'object\', '
                    '\'color\', '
                    '\'intensity\', '
                    '\'mount\''
                    )
        raise KeyError(error_msg) 

    color_desc = desc['color']
    expected_keys = ['r', 'g', 'b', 'alpha']
    keys_status = [key in color_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for tube color dictionary keys. '
                    'Expected keys: \'r\', \'g\', \'b\', \'alpha\''
                    )
        raise KeyError(error_msg)

    if 'size' not in desc['mount']:
        error_msg = (
                    'Wrong schema for tube mount dictionary keys. '
                    'Expected keys: \'size\''
                    )
        raise KeyError(error_msg)

    mount_size_desc = desc['mount']['size']
    print(mount_size_desc)
    expected_keys = ['x', 'y', 'z']
    keys_status = [key in mount_size_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for tube mount size dictionary keys. '
                    'Expected keys: \'x\', \'y\', \'z\''
                    )
        raise KeyError(error_msg)


def validate_simple_spot_schema(desc = {}):
    """
    Raises an exception if the frame schema used for input is badly formatted 
    """
    expected_keys = [
                    'object', 
                    'color',
                    'intensity', 
                    'mount', 
                    'iesfile',
                    ]
    keys_status = [key in desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for tube dictionary keys. '
                    'Expected keys: '
                    '\'object\', '
                    '\'color\', '
                    '\'intensity\', '
                    '\'mount\''
                    '\'iesfile\''
                    )
        raise KeyError(error_msg) 

    color_desc = desc['color']
    expected_keys = ['r', 'g', 'b']
    keys_status = [key in color_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for spot color dictionary keys. '
                    'Expected keys: \'r\', \'g\', \'b\''
                    )
        raise KeyError(error_msg)

    if 'size' not in desc['mount']:
        error_msg = (
                    'Wrong schema for tube mount dictionary keys. '
                    'Expected keys: \'size\''
                    )
        raise KeyError(error_msg)

    mount_size_desc = desc['mount']['size']
    print(mount_size_desc)
    expected_keys = ['x', 'z']
    keys_status = [key in mount_size_desc for key in expected_keys]
    has_keys = reduce((lambda x, y: x and y), keys_status)
    if not has_keys:
        error_msg = (
                    'Wrong schema for spot mount size dictionary keys. '
                    'Expected keys: \'x\', \'z\''
                    )
        raise KeyError(error_msg)
