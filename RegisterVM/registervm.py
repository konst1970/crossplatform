import logging

#
# Cross Platform Virtual Machine
#
# R0 - R255 - 2 bytes, bigendian
#
# Bytecode: 0x00 - idle                             (1 byte)
#           0x01 - Load two bytes to Register B3    (4 bytes), bigendian
#           0x02 - Add B1 and B2 and place to B3    (4 bytes)
#           0x03 - Print B1                         (2 bytes)
#                  for instance 0x05 0x00 prints R1
#           0x04 - if B1 nonzero then jump to next B2 commands (3 bytes)

logger = logging.getLogger('my_logger')

logging.basicConfig(
    level=logging.DEBUG # allow DEBUG level messages to pass through the logger
    )

bytecode = [0x00,  # idle
            0x01,  # load 0xFF01 (65281) to R0 , bigendian
              0xFF, 
              0x01,
              0x00,  # R0
            0x01,  # load 0x02 to R1, bigendian
              0x00, 
              0x03,
              0x01,  # R1    
            0x02,  # add R0 to R1 and place to R2
              0x00,  # R0
              0x01,  # R1
              0x02,  # R2
            0x04, # Jump if nonzero
              0x00, # if R0 nonzero then jump to next R1 commands 
              0x01, # R1 where to jump
            0x00, # idle
            0x00, # idle
            0x00, # idle
            0x03,  # print R2
              0x02,  # R2
            0x00]  # idle

logging.debug(bytecode)

# command count
count = 0

# 256 Registers
nreg = 256
R = [0] * nreg

# Go through all bytes bytes

while (count < len(bytecode)):
    # logging.debug(bytecode[count])

    if (bytecode[count] == 0x00): # idle
      logging.debug("IDLE")
      count += 1
      continue

    if (bytecode[count] == 0x01): # load two bytes to R[addr]
      addr = bytecode[count+3]
      if (addr < nreg):
        R[addr] = bytecode[count+1]<<8 | bytecode[count+2]
        logging.debug("R"+str(addr)+"="+str(R[addr]))
      count += 4
      continue

    if (bytecode[count] == 0x02): # R3 = R1 + R2
      R[bytecode[count+3]] = R[bytecode[count+1]] + R[bytecode[count+2]]
      logging.debug("Rz = Rx + Ry, Rz="+str(R[bytecode[count+3]]))
      count += 4
      continue

    if (bytecode[count] == 0x03): # print R*
      logging.debug("PRINT")
      addr = bytecode[count+1]
      if (addr < nreg):
        print (R[addr])
        logging.debug(R[addr])
      count += 2
      continue

    if (bytecode[count] == 0x04): # If b1 is nonzero then jump to next b2
      logging.debug("Jump if B1 != 0 "+str(R[bytecode[count+1]]))
      if (R[bytecode[count+1]]):
        logging.debug("Jump to next B2 "+str(R[bytecode[count+2]]))
        count += R[bytecode[count+2]]  # this code is not safe
      count += 3
      continue

logging.debug("bytecode is completed")
