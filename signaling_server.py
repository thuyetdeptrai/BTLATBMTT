#!/usr/bin/env python

import asyncio
import websockets
import json
import logging

# --- Cấu hình logging chi tiết hơn ---
# Định dạng log để hiển thị thời gian, cấp độ và thông điệp
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
# Tránh thêm handler nhiều lần nếu script được import
if not logger.handlers:
    logger.addHandler(stream_handler)

# Dictionary để lưu các client đã kết nối: {client_id: websocket_object}
CONNECTED_CLIENTS = {}

async def unregister(client_id):
    """Xóa client khỏi danh sách khi ngắt kết nối."""
    if client_id and client_id in CONNECTED_CLIENTS:
        del CONNECTED_CLIENTS[client_id]
        logger.info(f"Client '{client_id}' đã được xóa khỏi danh sách.")

async def register(websocket):
    """
    Chờ và xử lý tin nhắn 'register' đầu tiên từ client.
    Trả về client_id nếu đăng ký thành công, ngược lại trả về None.
    """
    try:
        message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
        data = json.loads(message)

        if data.get('type') == 'register':
            client_id = data.get('id')
            if not client_id:
                await websocket.send(json.dumps({'type': 'error', 'message': 'ID không hợp lệ.'}))
                return None

            if client_id in CONNECTED_CLIENTS:
                await websocket.send(json.dumps({'type': 'error', 'message': f'ID "{client_id}" đã được sử dụng.'}))
                return None
            
            CONNECTED_CLIENTS[client_id] = websocket
            logger.info(f"Client '{client_id}' đã đăng ký thành công.")
            await websocket.send(json.dumps({'type': 'register_ok', 'id': client_id}))
            return client_id
        else:
            logger.warning("Tin nhắn đầu tiên không phải là 'register'.")
            return None
    except asyncio.TimeoutError:
        logger.warning("Không nhận được tin nhắn register trong 10 giây.")
        return None
    except Exception as e:
        logger.error(f"Lỗi trong quá trình đăng ký: {e}")
        return None


async def message_handler(websocket, client_id):
    """Vòng lặp xử lý các tin nhắn sau khi đã đăng ký thành công."""
    async for message in websocket:
        try:
            data = json.loads(message)
            recipient_id = data.get('to')
            
            if not recipient_id:
                logger.warning(f"Tin nhắn từ '{client_id}' không có người nhận ('to').")
                continue

            recipient_ws = CONNECTED_CLIENTS.get(recipient_id)
            
            if recipient_ws:
                data['from'] = client_id
                await recipient_ws.send(json.dumps(data))
                logger.info(f"Đã chuyển tiếp tin nhắn '{data.get('type')}' từ '{client_id}' đến '{recipient_id}'.")
            else:
                logger.warning(f"Không tìm thấy người nhận '{recipient_id}' cho tin nhắn từ '{client_id}'.")
                await websocket.send(json.dumps({'type': 'error', 'message': f'Không tìm thấy người dùng "{recipient_id}".'}))
        except Exception as e:
            logger.error(f"Lỗi khi xử lý tin nhắn từ '{client_id}': {e}")


# THAY ĐỔI: Sửa chữ ký của hàm, bỏ tham số 'path'
async def connection_handler(websocket):
    """
    Hàm chính xử lý mỗi kết nối mới từ client.
    """
    logger.info(f"Một client mới đã kết nối từ {websocket.remote_address}.")
    client_id = None
    try:
        client_id = await register(websocket)
        
        if client_id:
            await message_handler(websocket, client_id)

    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Kết nối với client '{client_id}' đã đóng (mã: {e.code}, lý do: {e.reason}).")
    except Exception as e:
        logger.error(f"Một lỗi không mong muốn đã xảy ra với client '{client_id}': {e}")
    finally:
        logger.info(f"Đang dọn dẹp cho client '{client_id}'.")
        await unregister(client_id)


async def main():
    async with websockets.serve(connection_handler, "localhost", 8765):
        logger.info("Signaling Server đã bắt đầu trên ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server đang tắt...")

