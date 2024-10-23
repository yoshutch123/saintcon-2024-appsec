package community.saintcon.appsec.utils;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Date;
import java.util.function.Function;

@Service
public class JwtUtil {

    private final String secret;
    private static final String ISSUER = "irc.local";

    public JwtUtil() throws IOException {
        this.secret = readSecretFromFile();
    }

    private String readSecretFromFile() throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("/run/secrets/app_secret"));
        return br.readLine();
    }

    public String generateToken(Long claimId, long expiryInMinutes) {
        return createToken(claimId.toString(), expiryInMinutes);
    }

    public Long getValidatedClaimId(String token) {
        if (!isTokenExpired(token)) {
            return getClaimFromToken(token, jwt -> Long.parseLong(jwt.getSubject()));
        }
        return null;
    }

    private Date extractExpiration(String token) {
        return getClaimFromToken(token, DecodedJWT::getExpiresAt);
    }

    private <T> T getClaimFromToken(String token, Function<DecodedJWT, T> claimsResolver) {
        final DecodedJWT jwt = decodeToken(token);
        return claimsResolver.apply(jwt);
    }

    private DecodedJWT decodeToken(String token) {
        return JWT.require(Algorithm.HMAC256(secret.getBytes()))
            .withIssuer(ISSUER)
            .build()
            .verify(token);
    }

    private Boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    private String createToken(String subject, Long expiryInMinutes) {
        return JWT.create()
                .withSubject(subject)
                .withIssuer(ISSUER)
                .withIssuedAt(new Date(System.currentTimeMillis()))
                .withExpiresAt(new Date(System.currentTimeMillis() + (expiryInMinutes * 60 * 1000)))
                .sign(Algorithm.HMAC256(secret.getBytes()));
    }

}
