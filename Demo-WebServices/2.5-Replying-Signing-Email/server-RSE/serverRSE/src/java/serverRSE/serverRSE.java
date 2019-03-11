/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package serverRSE;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.SecureRandom;
import java.security.Signature;
import java.security.SignatureException;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.Scanner;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.jws.WebService;
import javax.jws.WebMethod;
import javax.jws.WebParam;
import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;

/**
 *
 * @author HoangChuong
 */
@WebService(serviceName = "serverRSE")
public class serverRSE {
public static class ReturningKeyPair {

        private PublicKey pubKey;
        private PrivateKey priKey;

        public ReturningKeyPair(PublicKey pubKey, PrivateKey priKey) {
            this.pubKey = pubKey;
            this.priKey = priKey;
        }
    }
public static void main()
    {
        try{
        SecureRandom sr = new SecureRandom();
	
			KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
			kpg.initialize(1024, sr);
			KeyPair kp = kpg.genKeyPair();
			PublicKey publicKey = kp.getPublic();
			PrivateKey privateKey = kp.getPrivate();
			File publicKeyFile = createKeyFile(new File("D:/publicKey.rsa"));
			File privateKeyFile = createKeyFile(new File("D:/privateKey.rsa"));
			FileOutputStream fos = new FileOutputStream(publicKeyFile);
			fos.write(publicKey.getEncoded());
			fos.close();
			fos = new FileOutputStream(privateKeyFile);
			fos.write(privateKey.getEncoded());
			fos.close();      
        }
        catch(Exception e){
            
        }
    }
    private static File createKeyFile(File file) throws IOException {
		if (!file.exists()) {
			file.createNewFile();
		} else {
			file.delete();
			file.createNewFile();
		}
		return file;
	}
    /**
     * Web service operation
     */
    @WebMethod(operationName = "signatureRSE")
    public String signatureRSE(@WebParam(name = "id") String id, @WebParam(name = "name") String name, @WebParam(name = "category") String category, @WebParam(name = "lvl") String lvl, @WebParam(name = "complexity") String complexity) throws SignatureException, IOException, NoSuchAlgorithmException, InvalidKeyException {
        //TODO write your implementation code here:
         KeyPairGenerator keyGen = KeyPairGenerator.getInstance("DSA");
            SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
            keyGen.initialize(1024, random);
            String message = id+","+name+","+category+","+lvl+","+complexity;
           KeyPair keyPair = keyGen.generateKeyPair();
            PrivateKey privateKey = keyPair.getPrivate();

            // Get an instance of Signature object and initialize it.
            Signature signature = Signature.getInstance("SHA256withDSA");
            signature.initSign(privateKey);
                byte[] bytes = message.getBytes(); // Your evaluation form for signing.
                signature.update(bytes);
       //     byte[] bytes = Files.readAllBytes(Paths.get("D:/DontMindMe.txt")); -----------This code doesn't copy the content file to bytes content.
    
            
            byte[] digitalSignature = signature.sign(); 
             String writedown = new BASE64Encoder().encode(digitalSignature);
    
            // Save digital signature and the public key to a file.
           
            Files.write(Paths.get("D:/Cpublickey.rsa"), keyPair.getPublic().getEncoded());
            return "Data signed = "+writedown;
    }

    /**
     * Web service operation
     */
    @WebMethod(operationName = "encryption")
    public String encryption(@WebParam(name = "id") String id, @WebParam(name = "name") String name, @WebParam(name = "category") String category, @WebParam(name = "lvl") String lvl, @WebParam(name = "complexity") String complexity) throws IOException, InvalidKeySpecException, InvalidKeyException, NoSuchAlgorithmException, NoSuchPaddingException, IllegalBlockSizeException, BadPaddingException {
          FileInputStream fis = new FileInputStream("D:/publicKey.rsa");
			byte[] b = new byte[fis.available()];
			fis.read(b);
			fis.close();
			X509EncodedKeySpec spec = new X509EncodedKeySpec(b);
			KeyFactory factory = KeyFactory.getInstance("RSA");
			PublicKey pubKey = factory.generatePublic(spec);
			Cipher c = Cipher.getInstance("RSA");
			c.init(Cipher.ENCRYPT_MODE, pubKey);
                        
                      String result = id+","+name+","+category+","+lvl+","+complexity;
                        
			byte encryptOut[] = c.doFinal(result.getBytes());
			String strEncrypt = Base64.getEncoder().encodeToString(encryptOut);
                        return "Data encrypted = "+strEncrypt;
    }

    /**
     * Web service operation
     */
    @WebMethod(operationName = "verificationRSE")
    public String verificationRSE(@WebParam(name = "signedData") String signedData, @WebParam(name = "encryptedData") String encryptedData) throws IOException, NoSuchAlgorithmException, InvalidKeySpecException, InvalidKeyException, SignatureException, NoSuchPaddingException, IllegalBlockSizeException, BadPaddingException {
         byte[] publicKeyEncoded = Files.readAllBytes(Paths.get("D:/Cpublickey.rsa")); // <------ Public key of supervisor
         //   byte[] digitalSignature = Files.readAllBytes(Paths.get("D:/signature.txt"));
          
                BASE64Decoder decoder = new BASE64Decoder();
            byte[] digitalSignature = decoder.decodeBuffer(signedData);
            X509EncodedKeySpec publicKeySpec = new X509EncodedKeySpec(publicKeyEncoded);
            KeyFactory keyFactory = KeyFactory.getInstance("DSA");

            PublicKey publicKey = keyFactory.generatePublic(publicKeySpec);
            Signature signature = Signature.getInstance("SHA256withDSA");
            signature.initVerify(publicKey);

    //        byte[] bytes2 = Files.readAllBytes(Paths.get("D:/Dawn.txt")); // Email Server Evaluation Form
    
    FileInputStream fis = new FileInputStream("D:/privateKey.rsa"); // <----- private key Email Server
	byte[] b = new byte[fis.available()];
	fis.read(b);
	fis.close();
	PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(b);
	KeyFactory factory = KeyFactory.getInstance("RSA");
	PrivateKey priKey = factory.generatePrivate(spec);
	Cipher c = Cipher.getInstance("RSA");
	c.init(Cipher.DECRYPT_MODE, priKey);
	byte decryptOut[] = c.doFinal(Base64.getDecoder().decode(encryptedData));
        String strDecrypt = new String(decryptOut);
    
    //
            byte[] bytes2 = strDecrypt.getBytes();
            signature.update(bytes2); // hashed
            
            boolean verified = signature.verify(digitalSignature);
            System.out.println("Boolean = "+verified);
            if (verified) {
                System.out.println("Data verified.");
                
            } else {
                System.out.println("Cannot verify data.");
            }
        return "[true - Evaluation is verified] [false - Form is not correct]  Result : "+Boolean.toString(verified);
    }
}
