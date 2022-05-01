import matplotlib.pyplot as plt

xCoor = [13.05,  13.40,   13.0,  13.30,  13.03, 13.30]
yCoor = [13.05,  13.05,   13.05,  13.05,  13.05,  13.05]
zCoor = [0.1,   .1,   1.00,  1.00,  1.1,  1.5]

    #0 is R-ankle
    #1 is L-ankle
    #2 is R-wrist
    #3 is L-wrist
    #4 is R-hip 
    #5 is chest
x=["R-ankle","L-ankle","R-wrist","L-wrist","R-hip","Chest"]
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot(12.75,12.75,1)
ax.scatter(xCoor,yCoor,zCoor)
for i in range(len(x)):
    ax.text(xCoor[i],yCoor[i],zCoor[i],x[i])
ax.scatter(13,12,.5,"green")
ax.text(13,12,.5,"Hub")

ax.scatter(13.6,5,.2,"s")
ax.text(13.6,5,0.2,"attacker")
ax.plot(13.6,13.05,1)
plt.xlabel("x")
plt.ylabel("y")


plt.show()


