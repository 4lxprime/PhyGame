<?php

function add_kill($usr) {

    global $conn;

    $sql="SELECT kills FROM users WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);
    $row=mysqli_fetch_assoc($result);

    $nkill=$row['kills'];
    $lkill=$nkill+1;

    $sql="UPDATE users SET kills='$lkill' WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        
        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {
        
        echo json_encode("error", JSON_PRETTY_PRINT);

    }

}

?>