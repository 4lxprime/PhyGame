<?php

function ban($usr, $token) {

    global $conn;

    $sql="SELECT status FROM users WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);
    $stat=mysqli_fetch_assoc($result);

    if ($stat['status']=="ban") {
        
        echo json_encode("already_ban", JSON_PRETTY_PRINT);

    } else if ($stat['status']=="normal") {
        $sql="UPDATE users SET status='ban' WHERE username='$usr' AND token='$token'";
        $result=mysqli_query($conn, $sql);

        if ($result==TRUE) {
            
            echo json_encode("ban", JSON_PRETTY_PRINT);

        } else {
            
            echo json_encode("ban_error", JSON_PRETTY_PRINT);
        }
    }
}

function unban($usr, $token) {
    
    global $conn;

    $sql="SELECT status FROM users WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);
    $stat=mysqli_fetch_assoc($result);

    if ($stat['status']!="ban") {
        
        echo json_encode("already_unban", JSON_PRETTY_PRINT);

    } else if ($stat['status']=="ban") {
        $sql="UPDATE users SET status='normal' WHERE username='$usr' AND token='$token'";
        $result=mysqli_query($conn, $sql);

        if ($result==TRUE) {
            
            echo json_encode("unban", JSON_PRETTY_PRINT);

        } else {
            
            echo json_encode("unban_error", JSON_PRETTY_PRINT);
        }
    }
}

?>