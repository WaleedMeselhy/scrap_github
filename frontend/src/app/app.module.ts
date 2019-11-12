import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { AppComponent } from "./app.component";
import { HttpClientModule } from "@angular/common/http";
import { ReposListComponent } from "./repos/repos-list/repos-list.component";
import { TagInputModule } from "ngx-chips";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { ReposSearchComponent } from "./repos/repos-search/repos-search.component";
import { AppRoutingModule } from "./app-routing.module";
import { RepoDetailsComponent } from './repos/repo-details/repo-details.component';
import { ReposComponent } from './repos/repos.component';
@NgModule({
  declarations: [AppComponent, ReposListComponent, ReposSearchComponent, RepoDetailsComponent, ReposComponent],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    TagInputModule,
    BrowserAnimationsModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
