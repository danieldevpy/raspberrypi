import asyncio
from websockets.server import serve
from threading import Thread
from cam import CamModule
import cv2

conexoes = set()
cam = CamModule(0)
Thread(target=cam.run).start()

async def echo(websocket, path):
  conexoes.add(websocket)
  
  try:
      async for message in websocket:
          # Processar mensagens recebidas, se necessário

          # Enviar mensagens para todas as conexões
          for ws in conexoes:
              await ws.send(message)  # Envie a mensagem para todas as conexões

  except Exception as e:
      print(f"Erro na conexão: {e}")

  finally:
      # Remova a conexão WebSocket da lista quando a conexão for encerrada
      conexoes.remove(websocket)


async def main():
    async with serve(echo, "0.0.0.0", 8000):
        await asyncio.Future()  # run forever

async def enviar_mensagens():
    while True:
        if cam.last_frame is not None and conexoes:
          ret, buffer = cv2.imencode('.jpg', cam.last_frame)
          if ret:
            print(buffer)
            for conexao in conexoes:
              await conexao.send(buffer.tobytes())
        await asyncio.sleep(0.001)

async def main_with_tasks():
    await asyncio.gather(main(), enviar_mensagens())

if __name__ == "__main__":
    asyncio.run(main_with_tasks())
