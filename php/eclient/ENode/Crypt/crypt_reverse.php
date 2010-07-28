<?php

class CryptReverse
{

    public function Decrypt( $input ){
        $input->data = strrev( $input->data ) ;
        return $input ;
    }

}
