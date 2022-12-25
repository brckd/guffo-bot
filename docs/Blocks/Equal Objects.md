Outputs *True* if both object inputs are equal. Since object inputs default to None, just leave the second input empty to check if the first input is None.

[[uploads/Equal_Object.png]]

## Notes

* This checks if the two inputs are the same *[[blocks/object]]*, not whether they're the same *[[blocks/block]] type*. E.g. two [[blocks/Box]] blocks, placed in the world, will create two different and independently moving objects, so they are not equal despite both being made from the same block type.