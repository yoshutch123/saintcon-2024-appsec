package community.saintcon.appsec.utils;

import org.mindrot.jbcrypt.BCrypt;
import org.springframework.stereotype.Component;

@Component
public class CryptoUtil {
    public String hashPassword(String password) {
        return BCrypt.hashpw(password, BCrypt.gensalt());
    }

    public Boolean comparePassword(String password, String hash) {
        return BCrypt.checkpw(password, hash);
    }
}
