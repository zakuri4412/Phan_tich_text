package com.example.textanalysis;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;

@RestController
@RequestMapping("api/news")
@CrossOrigin(origins = "http://localhost:3000")
public class NewsController {

    @Autowired
    private RestTemplate restTemplate;

    @PostMapping("/process")
    @ResponseBody
    public ResponseEntity<?> processNews(@RequestParam String category) {
        String apiURL = "https://newsapi.org/v2/everything?q=" + category + "&apiKey=18e95069ef694d88b841caa177f60a26";
        ResponseEntity<String> res = restTemplate.getForEntity(apiURL, String.class);
        if (res.getStatusCode() == HttpStatus.OK) {
            String pythonAPI = "http://localhost:5000/process";
            HttpHeaders headers= new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            System.out.print(res.getBody());
            String filterRes = res.getBody().replace("[Removed]", "");
            HttpEntity<String> req = new HttpEntity<String>(filterRes, headers);

            ResponseEntity<String> pythonRes = restTemplate.postForEntity(pythonAPI, req, String.class);

            return ResponseEntity.ok(pythonRes.getBody());
        }
        return ResponseEntity.status(res.getStatusCode()).body("Error when calling NewsAPI");
    }


}