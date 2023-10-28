import asyncio
from websockets.server import serve
from threading import Thread
from cam import CamModule
import cv2

conexoes = set()
cam = CamModule(0)

async def echo(websocket, path):
  conexoes.add(websocket)
  print(websocket)
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
    remove = None
    while True:
        if conexoes:
          cam.capture()
          ret, buffer = cv2.imencode('.jpg', cam.last_frame)
          bytes_array = buffer.tobytes()
          for conexao in conexoes:
            try:
              await conexao.send(bytes_array)
            except:
              remove = conexao
          if remove:
             conexoes.remove(remove)
             remove = None
          await asyncio.sleep(0)

async def main_with_tasks():
    await asyncio.gather(main(), enviar_mensagens())

if __name__ == "__main__":
    asyncio.run(main_with_tasks())
