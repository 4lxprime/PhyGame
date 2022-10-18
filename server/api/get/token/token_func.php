<?php

function token_get($usr, $pass) {

    global $conn;

    $sql="SELECT password FROM users WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);

    if (mysqli_num_rows($result)!=0) {
        $row=mysqli_fetch_assoc($result);

        if ($row['password']==$pass) {
            $sql="SELECT token FROM token WHERE password='$pass'";
            $result=mysqli_query($conn, $sql);
            
            if (mysqli_num_rows($result)!=0) {
                $row=mysqli_fetch_assoc($result);
                $sql="SELECT token FROM users WHERE username='$usr' AND password='$pass'";
                $result=mysqli_query($conn, $sql);

                if (mysqli_num_rows($result)!=0) {
                    $oldtkn=$row['token'];
                    $token=hash('sha256', $oldtkn);
                    $token=hash('sha512', $token);
                    $row=mysqli_fetch_assoc($result);
                    
                    if ($token==$row['token']) {

                        echo json_encode($oldtkn, JSON_PRETTY_PRINT);

                    } else {

                        echo json_encode("error", JSON_PRETTY_PRINT);
        
                    }

                } else {

                    echo json_encode("error", JSON_PRETTY_PRINT);
    
                }

            } else {

                echo json_encode("error", JSON_PRETTY_PRINT);

            }

        } else {

            echo json_encode("error", JSON_PRETTY_PRINT);

        }

    } else {

        echo json_encode("error", JSON_PRETTY_PRINT);

    }

}

?>