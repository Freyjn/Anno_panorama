# Anno_panorama
Skyscraper population optimization in Anno 1800

Requirements

This program is written in Python so if you want to use it you need to have Python download. If you don’t have it, you can find everything on the internet but remember you need three things: Python itself, an interpreter like Pyzo and a package library like Conda or MiniConda. You can find everything explained on the internet.
You will also need the Anno Designer software, which can also be easily found on the Anno 1800 Wiki website. It is an amazing tool that allows you to design layouts for every Anno game, and in our case for Anno 1800.

Program in a nutshell

Here are the steps you have to follow to use the program:
1.	Use Anno Designer to design your layout. Place only Old World residences which code is A7_resident! If you use any other kind of residence, it won’t work. Don’t place any other building nor roads (you can place them to help you design the layout, but when you save the file they must be deleted).
2.	Save your file as “ layout.txt “ in your C:User/User directory.
3.	Open the program with Pyzo (or any other Python interpreter) and execute the optimization(nbr_iter,nbr_try) function. You will have to give 2 parameters: nbr_iter is the number of iterations of the optimization process, it should be at least equal to three times the number of houses you placed in your layout; nbr_try is the number of time you are running the optimization program, the higher it is the better final layout you will get.
4.	When the program has finished, it will tell you the maximum population it was able to reach. Open your layout.txt file with Anno Designer. The tier of each skyscraper is given by its color: cyan for tier 5, magenta for tier 4, yellow for tier 3, blue for tier 2, green for tier 1 and red for tier 0 (normal house).
5.	Think about your result! This program does not give the layout with the highest population but one with a close population. So before you apply the layout to your game, think about it, especially for low tier skyscrapers: is it possible to increase their tier without messing up with the solution. An example of this critical thinking is given in figure 6  of the Advanced program understanding section.
