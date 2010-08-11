<?php

class InputRandom
{

    private $onInput ;
    public $inputData ;
    private $ENode ;
    private $Database ;

    public function __construct () {
        //$this->Type = "random" ;
    }

    public function registerDataBase ( $Database_ ) {
        $this->Database = $Database_ ;
    }

    public function registerOnInput( &$ENode, $onInputName ){
        $this->ENode = &$ENode ;
        $this->onInput = $onInputName ;
        //echo "function: ".$onInputName ;
        //echo $this->onInput ;

        // Name->"name", function->function
        //$this->ProcessRequests = $this->Process->ProcessTokens ;
    }

    public function checkInput(){
        
        $this->inputData = '<erequest type="messenger" id="0">
  <body>
   <subtype>message</subtype>
   <text>Hello World!</text>
   <format></format>
  </body>
  </erequest>' ;
        $func = $this->onInput ;
        $this->ENode->$func ( $this->inputData ) ;
    }

}
