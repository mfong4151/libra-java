
package com.linkedin.voyager.dash.conversations.services;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * A very small REST endpoint that responds to GET /api/hello with “Hello, world!”.
 */
@RestController
@RequestMapping("/api/hello")
public class MockClass {

    @GetMapping
    public ResponseEntity<String> sayHello() {
        return ResponseEntity.ok("Hello, world!");
    }
}
