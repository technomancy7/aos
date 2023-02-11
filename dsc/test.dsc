
@name Artists
+names Eminem
+names Linkin Park

start Eminem
+songs Lose Yourself
+songs Not Afraid
end

@copy_of_name @{name}

@first_artist @{names#0}

#echo My favourite artist is @{first_artist}, and his song @{Eminem.songs#0}
#delay 2.5
#echo Now, a couple seconds later, we winning.
#aos test