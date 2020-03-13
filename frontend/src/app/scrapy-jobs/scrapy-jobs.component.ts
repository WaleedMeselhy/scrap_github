import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";

import { NgForm } from "@angular/forms";

@Component({
  selector: "app-scrapy-jobs",
  templateUrl: "./scrapy-jobs.component.html",
  styleUrls: ["./scrapy-jobs.component.css"]
})
export class ScrapyJobsComponent implements OnInit {
  constructor(private http: HttpClient) {}

  ngOnInit() {}
  on_submit(form: NgForm) {
    let data = { url: form.value.url };
    console.log(data);

    this.http
      .post("http://localhost:5000/scrapyjob/", data)
      .subscribe(response => {
        console.log(response);
      });
    form.reset();
  }
}
