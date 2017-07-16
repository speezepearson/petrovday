A lot of people in my bubble celebrate [Petrov Day](http://lesswrong.com/lw/jq/926_is_petrov_day/), the day when [Stanislav Petrov](https://en.wikipedia.org/wiki/Stanislav_Petrov) (an officer keeping watch over a Soviet early-warning system) decided not to inform his superiors when his instruments (incorrectly, as it later turned out) indicated that the United States had just launched several nukes at Russia. If he had sounded the alarm, Russia might have retaliated, conceivably ending the world.

What would a Petrov Day celebration be without a little... thematic fun?


Petrov Day: a game for 2 or more teams
======================================

The game is played mostly passively. While you hold your Petrov Day party, you have a browser tab sitting open in the background, connected to the server administering the game; your opponents, holding their own parties; do the same. Each party's goal is to not get nuked, while finishing the game with as few remaining opponents as possible.

At any point, you can click a button to launch a nuke at any of your opponents. The victim has an early warning system (EWS) that will quickly detect that you've launched, and they'll have about one minute to decide whether to retaliate. The reason they might *not* retaliate is that EWSs are not perfectly reliable. If they "retaliate" in response to a false alarm, you might launch *for real.* So at some point during the evening, you might get a frantic call from one of your opponents, asking whether you just launched and listening for any deceit in your voice as you assure them that you did not.

If your friends are all too nice, and you know they won't really nuke you, set up some kind of incentive to eliminate your opponents. Maybe arrange for a pot of money to be distributed between the surviving teams at the end of the evening.

**Hardcore mode:** if you get nuked, the party is over. Everybody packs up in silence and goes home.


### Early Warning System specification

You have an EWS pointing at each enemy power. An EWS measures... something-or-other radiation, the kids in the lab had a fancy name for it. Anyway, the important part is, missiles emit heckloads of it! If you have your EWS trained on somebody who launches a missile at you, the readings will go up and up and up until it, uh, lands. And if they launch at somebody else, you'll see a spike at first, but it will drop off.

Unfortunately, there's some level of background radiation and measurement noise, which fluctuates quite a bit, and once in a while, it might look like they've launched when they haven't. C'est la vie.
