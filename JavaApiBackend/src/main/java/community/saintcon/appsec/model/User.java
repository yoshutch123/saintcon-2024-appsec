package community.saintcon.appsec.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties; 


@JsonIgnoreProperties({ "password" })
public record User(long userId, String name, String username, String password, boolean banned) {
}
