Date Formatting: MM/DD/YYYY

# 07/25/2025
I should probably use ISO 8601 but I don't care so I just clarified ahead.<br />
First day, need to actually learn how this stuff works and will avoid AI.<br />
No AI. At all. Or I will try not to use AI. I swear I won't lie if I do.<br />
Okay, I have decided to use Pymunk as my physics engine becaues it's a popular choice.

Credits for day one: https://youtu.be/YrNpkuVIFdg

# 07/27/2025

I will admit that I used a very, very, small amount of AI.<br />
I spent 2 hours trying to get it to work so I just got mad
but the changes were only three lines so don't kill me pls.<br />
The changes from AI were lines 18 and 28.<br />
Also line 20 on the position (2nd) parameter.

But it works now so yay. I feel guilty though, I'm sorry guys.

# 07/28/2025

Okay, I used AI again but in my defense it didn't solve anything really.<br />
I swear that I only used AI for like the last 5 mins and it was all because of a stupid typo.<br />
I coded everything else by myself by doing research. What AI pointed out was that I was calling the first value of the y axis of the apple.<br />
This is what it looked like before and after AI:
```
# Before:
render += cv2.warpAffine(img, np.float32([[1,0,(list(map(int, apple.body.position))[0]-250)],[0,1,(list(map(int, apple.body.position))[0]-250)]]), (512, 512))
# After:
render += cv2.warpAffine(img, np.float32([[1,0,(list(map(int, apple.body.position))[0]-250)],[0,1,(list(map(int, apple.body.position))[1]-250)]]), (512, 512))
```
But anyways the changes I made was only adding a plane image to OpenCV which was way harder than I thought. Spent a whole hour just on that.

# 08/09/2025

Wow, it has been a while since I touched this project.<br />
Well anwyays, I added user input to control some variables and renamed some variables and functions.<br />
And this time I did NOT use AI. This update is too easy to use it anyways.<br />
Next I need to add altitude and all that stuff but whatever.

# 08/10/2025

I didn't know terminal craft was ending today so I had to lock in.<br />
I mostly ditched Pymunk and only used it to store bodies, I think.<br />
And I will admit, I used AI for basically every formula because I didn't feel like searching it up.<br />
Also used AI to beautify my code but that is it.<br />
I'll be honest, the sim is still pretty bad so I will continue working on it after a break.<br />
This will just be v1, the bare functioning parts.<br />
I need to make it look better next time but for now I am going to rest my eyes and add documentation later to log more time.<br />
