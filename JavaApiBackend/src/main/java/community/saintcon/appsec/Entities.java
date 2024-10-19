package community.saintcon.appsec;

public class Entities {
    public record AuthenticationRequest(String username, String password) {
    }

    public record RegisterRequest(String username, String password, String name) {
    }

    public record CreateRoomRequest(String name) {
    }

    public record UpdateRoomRequest(String name, Long hostId) {
    }

    public record UpdateUserRequest(String username, String password, String name) {
    }

    public record AddUserToRoomRequest(String username, Long roomId) {
    }
}
