<?php

class DBDummy
{

    private $onListen ;
    private $listenData ;

    public function registerDataBase( &$onListen ){
        $this->onListen = &$onListen ;

        // Name->"name", function->function
        $this->ProcessRequests = $this->Process->ProcessTokens ;
    }

    public function Inject( $input ){
        $this->listenData = $input ;
        $this->onListen () ;
    }

}
