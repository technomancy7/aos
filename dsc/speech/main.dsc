start default
+respond Sorry, what was that?
end

start greeting
@trigger hello
+respond Hello there!
+respond Howdy!
+respond Ello.
end

start greeting2
<<greeting
@trigger hi
end

start personal greeting
@trigger hi ([\w]*) to (.*)
+respond Hello <0> to you too, <1>!
@weight 2
end

start personal greeting0
@trigger hi (.*)
+respond Hello <0> to you too!
@weight 1
end

start show config
@trigger show config
+respond Okay.
@command conf list
end

start set config
@trigger set ([\w]*) to (.*)
+respond Set <0> to <1>.
@command conf set <0> <1>
end

start set config 2
@trigger set ([\w]*) in ([\w]*) to (.*)
+respond Set <1>.<0> to <2>.
@command conf set <1>.<0> <2>
end

start diceroll
@trigger roll a dice
@command rng dice
end

start flip a coin
@trigger flip a coin
@command rng flip
end

start run app
@trigger run ([\w]*)
+respond Running <0>.
@command appman run <0>
end

start dear diary
@trigger dear diary
@command journal new
end

start add note
@trigger write a note
@command notes new -f
end

start scan directory
@trigger scan here for (.*)
@command scan <0>
end

start translator
@trigger translate (.*)
@command tr <0> --to:en --from:auto
end