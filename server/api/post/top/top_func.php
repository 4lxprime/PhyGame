<?php

include '../exp/exp_func.php';

function top1($usr, $token) {

    global $conn;

    $sql="SELECT top1 FROM stat WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        $row=mysqli_fetch_array($result);
        $oldtop1=$row['top1'];
        $top1=$oldtop1+1;
        sendD($usr, "top 1");

        $sql="UPDATE stat SET top1='$top1' WHERE username='$usr' AND token='$token'";
        $result=mysqli_query($conn, $sql);

        if ($result==TRUE) {
            
            get_mtx(1000, $usr);
            add_lvl(1, $usr, $token);


        } else {
            
            echo json_encode("error", JSON_PRETTY_PRINT);
        }

    } else {
        
        echo json_encode("error 1", JSON_PRETTY_PRINT);
    }

}

function top10($usr, $token) {

    global $conn;

    $sql="SELECT top10 FROM stat WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        $row=mysqli_fetch_array($result);
        $oldtop10=$row['top10'];
        $top10=$oldtop10+1;

        $sql="UPDATE stat SET top10='$top10' WHERE username='$usr' AND token='$token'";
        $result=mysqli_query($conn, $sql);

        if ($result==TRUE) {
            
            add_exp(5000, $usr, $token);
            get_mtx(100, $usr);

        } else {
            
            echo json_encode("error", JSON_PRETTY_PRINT);
        }

    } else {
        
        echo json_encode("error", JSON_PRETTY_PRINT);
    }

}

function top25($usr, $token) {

    global $conn;

    $sql="SELECT top25 FROM stat WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        $row=mysqli_fetch_array($result);
        $oldtop25=$row['top25'];
        $top25=$oldtop25+1;

        $sql="UPDATE stat SET top25='$top25' WHERE username='$usr' AND token='$token'";
        $result=mysqli_query($conn, $sql);

        if ($result==TRUE) {
            
            add_exp(2500, $usr, $token);
            get_mtx(50, $usr);

        } else {
            
            echo json_encode("error", JSON_PRETTY_PRINT);
        }

    } else {
        
        echo json_encode("error", JSON_PRETTY_PRINT);
    }

}

function kill($usr, $token) {

    global $conn;

    $sql="SELECT kills FROM stat WHERE username='$usr' AND token='$token'";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {
        $oldkills=mysqli_fetch_array($result);
        $kills=$oldkills['kills']+1;

        $sql="UPDATE stat SET kills='$kills' WHERE username='$usr' AND token='$token'";
        $result=mysqli_query($conn, $sql);

            if ($result==TRUE) {
                
                add_exp(1000, $usr, $token);

            } else {
                
                echo json_encode("error", JSON_PRETTY_PRINT);
            }

    } else {
        
        echo json_encode("error", JSON_PRETTY_PRINT);
    }

}

?>