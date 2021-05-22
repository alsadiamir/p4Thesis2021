// js for sample app custom view
(function () {
    'use strict';

    // injected refs
    var $log, $scope, wss, ks;

    // constants
    var dataReq = 'sampleCustomDataRequest',
        dataResp = 'sampleCustomDataResponse',
        dataEraseReq = 'eraseDataRequest',
        dataEraseResp = 'eraseDataResponse',
        dataCheckReq = 'owdDataRequest',
        dataCheckResp = 'owdDataResponse';

    function addKeyBindings() {
        var map = {
            space: [getData, 'Fetch data from server'],

            _helpFormat: [
                ['space']
            ]
        };

        ks.keyBindings(map);
    }

    function getData() {
        wss.sendEvent(dataReq);
    }

    function removeFile() {
        wss.sendEvent(dataEraseReq);
    }

    function checkOWD() {
        wss.sendEvent(dataCheckReq);
    }

    function respDataCb(data) {
        $scope.data = data;
        $scope.$apply();
    }


    angular.module('ovSampleCustom', [])
        .controller('OvSampleCustomCtrl',
        ['$log', '$scope', 'WebSocketService', 'KeyService',

        function (_$log_, _$scope_, _wss_, _ks_) {
            $log = _$log_;
            $scope = _$scope_;
            wss = _wss_;
            ks = _ks_;

            var handlers = {};
            $scope.data = {};

            // data response handler
            handlers[dataResp] = respDataCb;
            handlers[dataEraseResp] = respDataCb;
            handlers[dataCheckResp] = respDataCb;
            wss.bindHandlers(handlers);

            addKeyBindings();

            // custom click handler
            $scope.getData = getData;
            $scope.removeFile = removeFile;
            $scope.checkOWD = checkOWD;

            // get data the first time...
            getData();

            // cleanup
            $scope.$on('$destroy', function () {
                wss.unbindHandlers(handlers);
                ks.unbindKeys();
                $log.log('OvSampleCustomCtrl has been destroyed');
            });

            $log.log('OvSampleCustomCtrl has been created');
        }]);

}());
