         addi s1, x0, 1         # 1, 0x00, s1 = 1
         addi s0, x0, -1        # 2, 0x04, s0 = -1
label5:  beq  x0, x0, label1    # 3, 0x08
label6:  bltu x0, s0, label8    # 9, 0x0C
label4:  blt  s1, x0, label5    # 7, 0x10
         beq  x0, x0, label6    # 8, 0x14
label3:  beq  s1, s1, label4    # 6, 0x18
label10: beq  s0, s0, end       # 13, 0x1C
label2:  blt  x0, s1, label3    # 5, 0x20
label9:  blt  s0, s1, label10   # 12, 0x24
label1:  beq  x0, x0, label2    # 4, 0x28
label8:  bltu s1, s1, label9    # 10, 0x2C
         beq  s1, s1, label9    # 11, 0x30
end:     addi s0, x0, 2         # 14, 0x34
