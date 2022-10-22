<?php

function get_kill($usr) {

    global $conn;

    $sql="SELECT kills FROM users WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);

    if (mysqli_num_rows($result)!=0) {
      $row=mysqli_fetch_assoc($result);
      echo json_encode($row);

    }

}

?>