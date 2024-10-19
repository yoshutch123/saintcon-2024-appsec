package community.saintcon.appsec.model;

public record User(long userId, String name, String username, String password, boolean banned) {
}
