The Menu Item block is a script block which was added on Fancade 1.6. When it is  executed at least once it activates the shop system adding a shop to the game which is *only accessible when you win or lose the game.* The main use of this script is to add items to a shop which should only be done **once** per item. To learn how to use it, see [[here|script/How to use the shop system?]].

[[uploads/Menu_Item.png | width=336px]]

## Notes
Though this new script made a great new mechanic for Fancade it has some limitations:
* The base prices are currently only fixed to 10, 100, 1k & 10k.
* Each menu item script **must** only be executed once per game, if it's left continuously executing the shop will be filled with repeating set of items until it has too many items in it, which will cause the `Too many menu items!` error to appear.

## More info
Items can be either one type of upgrades or boosters just by playing with the buy limit settings and Variable input of the menu item script. You can choose between ON/OFF, Max 2-100 or no limit.

You also cannot use menu item to add buttons on the top of the screen or the pause menu. Remember the [[top of this page|#top]]?

## Example usage: Clicker game
You can make a clicker game with Menu Item. First, add a [[Blocks/Touch Sensor]] block, a [[Get Number Variable|Blocks/Get Variable]] block, an [[Blocks/Increase Number]] block and this script (Menu Item). Make it detect when 1st tap begins. Make it increase two variables: one named `Coins` and another one named `!Score`. (! means saved variable, tap `Local` then `Global` to get `Saved`.)

Now get a [[Blocks/Set Score]] block, plug in `!Score` into the Score wire, and plug `Coins` into the Coins wire.

Add a shop with some items, starting with `More per tap`. This is like in Fanclicker by Origedit. Replace the increase number with:

[[uploads/Screenshot_20220101-201031.png]]

Do the same for the `Coins` variable.

Add a way to make the player claim the coins they got in game and to submit their score. If you are using an object to do this then check if the object has no other object around it or is unglued; if not, do so. If you don't know how to do it then check [[this article.|Build/How glue makes blocks stick together and form larger objects]] You may also need the [[Tap to pick closest object|Script/Tap to pick closest object]] article.