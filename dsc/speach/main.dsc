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