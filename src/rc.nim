# RECORD KEEPER
# Journal software
import std/os

var
   confDir = getConfigDir() & "RecordKeeper" 
   filePath = confDir / "journal.json"
   
proc main() =
    echo "RC"
    echo confDir
    echo filePath
main()
