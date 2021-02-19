import logging

logger = logging.getLogger('my_logger')

logging.basicConfig(
    level=logging.DEBUG # allow DEBUG level messages to pass through the logger
    )

bytecode = [0x00,  # idle
            0xFF,  # push
            0x01,  # 1
            0xFF,  # push
            0x02,  # 2
            0x01,  # add 
            0x00]  # idle

count = 0

stack = []

def push(elem):
  global stack
  stack = [elem] + stack

def pop():
  global stack
  stack.pop(0)

while (count < len(bytecode)):
  if (bytecode[count] == 0x00): # idle
      logging.debug("IDLE")
      count += 1
      logging.debug(stack)
      continue

  if (bytecode[count] == 0xFF): # push
      logging.debug("PUSH")
      push(bytecode[count+1])
      count += 2
      logging.debug(stack)
      continue

  if (bytecode[count] == 0x01): # add
      logging.debug("ADD")
      result = stack[0] + stack[1]
      pop()
      pop()
      count += 1
      push(result)
      logging.debug(stack)
      continue

  count +=1

