<?php 

function get_mtx($mtx, $usr) {

    global $conn;

    $sql="SELECT mtx FROM users WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);
    $row=mysqli_fetch_assoc($result);

    $nmtx=$row['mtx'];
    $mtx=$nmtx+$mtx;

    $sql="UPDATE users SET mtx='$mtx' WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        
        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {
        
        echo json_encode("nope", JSON_PRETTY_PRINT);
    }
}

function del_mtx($mtx, $usr) {
    global $conn;
    $sql="SELECT mtx FROM users WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);
    $row=mysqli_fetch_assoc($result);

    $nmtx=$row['mtx'];
    $mtx=$nmtx-$mtx;
    
    $sql="UPDATE users SET mtx='$mtx' WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);

    if ($result) {
        
        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {
        
        echo json_encode("nope", JSON_PRETTY_PRINT);
    }
}

?>