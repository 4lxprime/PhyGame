<?php 

include '../mtx/mtx_func.php';

function buy_item($item, $usr) {

    global $conn;

    $sql="SELECT item FROM users WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);
    $row=mysqli_fetch_assoc($result);

    $it=explode(", ", $row['item']);

    foreach($it as $i) {
        if ($i==$item) {
            echo json_encode("already_exist", JSON_PRETTY_PRINT);
            exit(0);
        } else {}
    }

    $sql="SELECT mtx FROM users WHERE username='$usr'";
    $result=mysqli_query($conn, $sql);
    $money=mysqli_fetch_assoc($result);

    $sql="SELECT item_price FROM item WHERE item_name='$item'";
    $result=mysqli_query($conn, $sql);
    $price=mysqli_fetch_assoc($result);

    if ($money['mtx'] > $price['item_price']) {
        $sql="SELECT item FROM users WHERE username='$usr'";
        $result=mysqli_query($conn, $sql);

        if (mysqli_num_rows($result)>0) {
            $row=mysqli_fetch_assoc($result);
            $items=$row['item'];
            $nitems=$items.', '.$item;
            $sql="UPDATE users SET item='$nitems' WHERE username='$usr'";
            $result=mysqli_query($conn, $sql);

            if ($result==TRUE) {
                get_mtx($price['item_price'], $usr);

            } else {
                echo json_encode("error", JSON_PRETTY_PRINT);

            }

        } else {
            $nitems=$item;
            $sql="UPDATE users SET item='$nitems' WHERE username='$usr'";
            $result=mysqli_query($conn, $sql);

            if ($result==TRUE) {
                get_mtx($price['item_price'], $usr);

            } else {
                echo json_encode("error", JSON_PRETTY_PRINT);

            }

        }

    } else {
        echo json_encode("not_money", JSON_PRETTY_PRINT);

    }
}

?>