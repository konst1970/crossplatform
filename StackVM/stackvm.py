import logging

logger = logging.getLogger('my_logger')

logging.basicConfig(
    level=logging.DEBUG # allow DEBUG level messages to pass through the logger
    )

bytecode = [0x00,  # idle
            0xFF,  # push
            0x01,  # 1 , (1 byte)
            0xFF,  # push
            0x02,  # 2 , (1 byte)
            0x01,  # add 
            0x00,  # idle
            0xFF,  # push 
            0x01,  # 1
            0x1F,  # if
            0x00,  # idle
            0x00,  # idle
            0x00,  # idle
            0x00   #idle
            ]

count = 0

stack = []

def push(elem):
  global stack
  stack = [elem] + stack

def pop():
  global stack
  return stack.pop(0) 

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
      result = pop() + pop()
      count += 1
      push(result)
      logging.debug(stack)
      continue

  if (bytecode[count] == 0x1F): # if nonzero
      logging.debug("IF")
      arg1 = pop()
      logging.debug(arg1)
      if (arg1):
        arg2 = pop()
        logging.debug(arg2)
        count += arg2
      count += 1
      logging.debug(stack)
      continue

  count +=1
