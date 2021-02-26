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
#           0x05 - Substrate B1 and B2 and place to B3 (4 bytes), bigendian
#           0xA0 - Define a function B1 - function ID, B2 - function length
#           0xA1 - Return from function
#           0xAA - Call function with ID stored in B1 

logger = logging.getLogger('my_logger')

logging.basicConfig(
    level=logging.DEBUG # allow DEBUG level messages to pass through the logger
    )

bytecode = [0x00,  # idle
            0x01,  # load 0xFF01 (65281) to R0 , bigendian
              0xFF, 
              0x00,
              0x00,  # R0
            0x01,  # load 0x0003 to R1, bigendian
              0x00, 
              0x03,
              0x01,  # R1    
            0x05,  # sub R0 to R1 and place to R2
              0x00,  # R0
              0x01,  # R1
              0x02,  # R2  /// R2 = R1 - R0
            0x01, # load
              0x00, # 0x0001
              0x01,
              0x03, # R3
            0x06, # Jump Ra > Rb
              0x00, # if R0 > R1  
              0x01, 
              0x03, # R1 where to jump
            0x00, # idle
            0x00, # idle
            0x00, # idle
            0x00, # idle
            0xA0, # function
              0x00, # function ID
              0x05, # lenght of function in bytes
                0x03, # print
                0x02, # R2
                0x00, # idle
                0xA1, # return (end of function)
                0x00, # The ID of the function we are returning from  
            0x01, # load
              0x00, # 0x0000
              0x00, # 
              0x00, # R0
            0xAA, # call function
              0x00, # R0 (function id)
            0x00, # idle
            0x00, # idle
            0x00, # idle
            0x00, # idle
            0x03,    # print R2
              0x02,  # R2
            0x00]    # idle

logging.debug(bytecode)

# command count
count = 0

#number of registers
nreg = 256


# 256 functions F[0] ... F[255]
function = {'id':0, 'length':0, 'addr':0, 'return_addr':0}
F = [0] * nreg

# 256 Registers  R[0] ... R[255]
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

    if (bytecode[count] == 0x05): # R3 = R1 - R2
      R[bytecode[count+3]] = R[bytecode[count+1]] - R[bytecode[count+2]]
      logging.debug("Rz = Rx - Ry, Rz="+str(R[bytecode[count+3]]))
      count += 4
      continue

    if (bytecode[count] == 0x03): # print R*
      logging.debug("PRINT")
      addr = bytecode[count+1]
      if (addr < nreg):
        print (R[addr])
        logging.debug("R " + str(addr) + "=" + str(R[addr]))
      count += 2
      continue

    if (bytecode[count] == 0x04): # If b1 is nonzero then jump to next b2
      logging.debug("Jump if B1 != 0 "+str(R[bytecode[count+1]]))
      if (R[bytecode[count+1]]):
        logging.debug("Jump to next B2 "+str(R[bytecode[count+2]]))
        count += R[bytecode[count+2]]  # this code is not safe
      count += 3
      continue

    if (bytecode[count] == 0x06): # If Ra > Rb jump to R3
      logging.debug("Jump if Ra > Rb "+str(R[bytecode[count+1]])+" "+str(R[bytecode[count+2]]))
      if (R[bytecode[count+1]] > R[bytecode[count+2]]):
        logging.debug("Jump to next Rc "+str(R[bytecode[count+3]]))
        count += R[bytecode[count+3]]  # this code is not safe
      count += 4
      continue
    
    if (bytecode[count] == 0xA0): # function
      logging.debug("FUNCTION " + str(bytecode[count+1]) + " length " + str(bytecode[count+2]))
      my_function = function
      my_function['id'] = bytecode[count+1]
      my_function['length'] = bytecode[count+2]
      my_function['addr'] = count
      F[my_function['id']] = my_function
      count = count + bytecode[count+2] + 3
      continue

    if (bytecode[count] == 0xA1): # return
      logging.debug("RETURN FROM FUNCTION ID " + str(bytecode[count+1]))
      my_function = F[bytecode[count+1]]
      count = my_function['return_addr']
      logging.debug("RETURN " + str(my_function['return_addr']))
      logging.debug("BYTECODE " + str(bytecode[my_function['return_addr']]))
      continue

    if (bytecode[count] == 0xAA): # call function
      logging.debug("CALL " + str(bytecode[1]))
      my_function = F[bytecode[count+1]]
      my_function['return_addr'] = count+2
      logging.debug("F " + str(my_function))
      count = my_function['addr']+my_function['length'] - 2

      logging.debug("count " + str(count) + " bytecode " + str(bytecode[count]))
      continue

logging.debug("bytecode is completed")
