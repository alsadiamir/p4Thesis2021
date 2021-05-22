/*
 * Copyright 2021-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.foo.app;

import com.fasterxml.jackson.databind.node.ObjectNode;
import com.google.common.collect.ImmutableSet;
import org.onosproject.ui.RequestHandler;
import org.onosproject.ui.UiMessageHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Collection;

/**
 * Skeletal ONOS UI Custom-View message handler.
 */
public class AppUiMessageHandler extends UiMessageHandler {

    private static final String SAMPLE_CUSTOM_DATA_REQ = "sampleCustomDataRequest";
    private static final String SAMPLE_CUSTOM_DATA_RESP = "sampleCustomDataResponse";

    private static final String ERASE_DATA_REQ = "eraseDataRequest";
    private static final String ERASE_DATA_RESP = "eraseDataResponse";

    private static final String OWD_DATA_REQ = "owdDataRequest";
    private static final String OWD_DATA_RESP = "owdDataResponse";

    private static final String OWD = "owd";
    private static final String MESSAGE = "message";

    private final Logger log = LoggerFactory.getLogger(getClass());

    @Override
    protected Collection<RequestHandler> createRequestHandlers() {
        return ImmutableSet.of(
                new SampleCustomDataRequestHandler(),
                new EraseRequestHandler()
                //new CheckOwdHandler()
        );
    }

    // handler for sample data requests
    private final class SampleCustomDataRequestHandler extends RequestHandler {

        private SampleCustomDataRequestHandler() {
            super(SAMPLE_CUSTOM_DATA_REQ);
        }

        @Override
        public void process(ObjectNode payload) {
            long owd = 0;
            long index = 0;
            BufferedReader reader;
            try {
                reader = new BufferedReader(new FileReader(
                        "/root/onos/apache-karaf-4.2.8/owd.txt"));
                String line = reader.readLine();
                while (line != null) {
                    //System.out.println(line);
                    log.info(line);
                    owd += Long.parseLong(line);
                    index++;
                    line = reader.readLine();
                }
                reader.close();
            } catch (IOException | NumberFormatException e) {
                e.printStackTrace();
            }

            log.debug("Computing owd for in file...");
            owd = owd / index;
            ObjectNode result = objectNode();
            result.put(OWD, "" + owd);
            sendMessage(SAMPLE_CUSTOM_DATA_RESP, result);
        }
    }

    // handler for sample data requests
    private final class EraseRequestHandler extends RequestHandler {

        private EraseRequestHandler() {
            super(ERASE_DATA_REQ);
        }

        @Override
        public void process(ObjectNode payload) {
            try {
                File f = new File("/root/onos/apache-karaf-4.2.8/owd.txt");           //file to be delete
                if (f.delete()) {
                    log.info(f.getName() + " deleted.");   //getting and printing the file name
                    ObjectNode result = objectNode();
                    result.put(OWD, "" + 0);
                    sendMessage(ERASE_DATA_RESP, result);
                } else {
                    log.error("Failed to delete owd.txt.");
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
/*
    // handler for sample data requests
    private final class CheckOwdHandler extends RequestHandler {

        private CheckOwdHandler() {
            super(OWD_DATA_REQ);
        }

        @Override
        public void process(ObjectNode payload) {
            try {
                String cmd = "util/mn-cmd h4 /mininet/send.py --dst_id 2 \"10.0.1.1\" \"ping\"";
                Runtime run = Runtime.getRuntime();
                run.exec(cmd);
                ObjectNode result = objectNode();
                result.put(MESSAGE, "OWD calculated successfully");
                sendMessage(OWD_DATA_RESP, result);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
*/
}


