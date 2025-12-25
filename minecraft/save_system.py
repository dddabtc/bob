# Minecraft 3D 存档系统
import json
import os
from settings3d import CHUNK_SIZE, WORLD_HEIGHT, BlockType


SAVE_DIR = os.path.join(os.path.dirname(__file__), 'saves')


def ensure_save_dir():
    """确保存档目录存在"""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


def save_game(world, player, filename='save.json'):
    """保存游戏"""
    ensure_save_dir()
    filepath = os.path.join(SAVE_DIR, filename)

    data = {
        'world': {
            'seed': world.seed,
            'one_block_mode': world.one_block_mode,
            'one_block_pos': world.one_block_pos,
            'blocks_mined': world.blocks_mined,
            'chunks': {}
        },
        'player': {
            'x': player.x,
            'y': player.y,
            'z': player.z,
            'yaw': player.yaw,
            'pitch': player.pitch,
            'health': player.health,
            'inventory': [],
            'selected_slot': player.selected_slot
        }
    }

    # 保存背包
    for item in player.inventory:
        if item is None:
            data['player']['inventory'].append(None)
        else:
            data['player']['inventory'].append([item[0], item[1]])

    # 保存区块（只保存被修改过的方块）
    for key, chunk in world.chunks.items():
        chunk_data = _serialize_chunk(chunk)
        if chunk_data:  # 只保存非空区块
            data['world']['chunks'][f"{key[0]},{key[1]}"] = chunk_data

    with open(filepath, 'w') as f:
        json.dump(data, f)

    print(f"游戏已保存到 {filepath}")
    return True


def load_game(world, player, filename='save.json'):
    """加载游戏"""
    filepath = os.path.join(SAVE_DIR, filename)

    if not os.path.exists(filepath):
        print(f"存档不存在: {filepath}")
        return False

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        # 恢复世界数据
        world.seed = data['world']['seed']
        world.one_block_mode = data['world']['one_block_mode']
        world.one_block_pos = tuple(data['world']['one_block_pos'])
        world.blocks_mined = data['world']['blocks_mined']

        # 清空现有区块并重新生成
        world.chunks.clear()
        world.generated_chunks.clear()

        # 恢复区块
        for key_str, chunk_data in data['world']['chunks'].items():
            cx, cz = map(int, key_str.split(','))
            chunk = world.get_chunk(cx, cz)  # 先生成基础区块
            _deserialize_chunk(chunk, chunk_data)  # 然后应用保存的修改

        # 恢复玩家数据
        player.x = data['player']['x']
        player.y = data['player']['y']
        player.z = data['player']['z']
        player.yaw = data['player']['yaw']
        player.pitch = data['player']['pitch']
        player.health = data['player']['health']
        player.selected_slot = data['player']['selected_slot']

        # 恢复背包
        player.inventory = []
        for item in data['player']['inventory']:
            if item is None:
                player.inventory.append(None)
            else:
                player.inventory.append((item[0], item[1]))

        # 重置速度
        player.vx = 0
        player.vy = 0
        player.vz = 0

        print(f"游戏已从 {filepath} 加载")
        return True

    except Exception as e:
        print(f"加载存档失败: {e}")
        return False


def _serialize_chunk(chunk):
    """序列化区块（只保存非空气方块）"""
    blocks = []
    for x in range(CHUNK_SIZE):
        for y in range(WORLD_HEIGHT):
            for z in range(CHUNK_SIZE):
                block = chunk.blocks[x][y][z]
                if block != BlockType.AIR:
                    blocks.append([x, y, z, block])

    return blocks if blocks else None


def _deserialize_chunk(chunk, blocks_data):
    """反序列化区块"""
    # 先清空区块
    for x in range(CHUNK_SIZE):
        for y in range(WORLD_HEIGHT):
            for z in range(CHUNK_SIZE):
                chunk.blocks[x][y][z] = BlockType.AIR

    # 恢复保存的方块
    for block_data in blocks_data:
        x, y, z, block_type = block_data
        chunk.blocks[x][y][z] = block_type

    chunk.dirty = True


def has_save(filename='save.json'):
    """检查存档是否存在"""
    filepath = os.path.join(SAVE_DIR, filename)
    return os.path.exists(filepath)
