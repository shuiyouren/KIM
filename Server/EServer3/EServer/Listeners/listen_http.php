<?php

class ListenHTTP
{

    private $Process ;

    public function registerProcess( &$Process ){
        $this->Process = &$Process ;
    }

    public function Inject( $input ){
        $this->Process ( $input ) ;
    }

}
