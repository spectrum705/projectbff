from twilio.rest import Client 
import os
from dotenv import load_dotenv
import yagmail

# DB_URI = os.getenv('DB_URI')  or os.environ["DB_URI"]
load_dotenv()


account_sid = os.getenv('account_sid') or os.environ["account_sid"]
auth_token  = os.getenv('auth_token') or os.environ["auth_token"]
messaging_service_sid = os.getenv('message_service_sid') or  os.environ["messaging_service_sid"]
gmail_id=os.getenv('gmail_id') or os.environ["gmail_id"]
gmail_password = os.getenv('gmail_password') or os.environ["gmail_password"]



def send_sms(to, body):
    sms_client = Client(account_sid, auth_token) 
    message = sms_client.messages.create(  
                            messaging_service_sid=messaging_service_sid, 
                            body=body,      
                            to=to 
                        ) 

def send_email(to, content, subject):
  yag = yagmail.SMTP(gmail_id, gmail_password)
  # contents = ['This is the body, and here is just text http://somedomain/image.png',
  #             'You can find an audio file attached.', '/local/path/song.mp3']
  yag.send(to, subject, content)


# send_email()
content="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Casper</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width" />
    <meta name="format-detection" content="telephone=no" />
    <style type="text/css">
      body {
        margin: 0 !important;
        padding: 0 !important;
        -webkit-text-size-adjust: 100% !important;
        -ms-text-size-adjust: 100% !important;
        -webkit-font-smoothing: antialiased !important;
      }
      img {
        border: 0 !important;
        outline: none !important;
        display: block !important;
      }
      p {
        margin: 0px !important;
        padding: 0px !important;
      }
      table {
        border-collapse: collapse;
        mso-table-lspace: 0px;
        mso-table-rspace: 0px;
      }
      td,
      a,
      span {
        border-collapse: collapse;
        mso-line-height-rule: exactly;
      }
      .ExternalClass * {
        line-height: 100%;
      }
      div {
        line-height: inherit !important;
      }
      .blue a {
        text-decoration: underline;
        color: #2f539f;
      }
      .em_link a {
        text-decoration: underline;
        color: #00237e;
      }
      td[class=em_aside] {
        padding-left: 10px !important;
        padding-right: 10px !important;
      }
      a {
        color: #999999;
      }
      @media only screen and (min-width:481px) and (max-width:600px) {
        table[class=em_wrapper] {
          width: 100% !important;
        }
        td[class=em_aside] {
          padding-left: 10px !important;
          padding-right: 10px !important;
        }
        td[class=em_hide],
        table[class=em_hide],
        span[class=em_hide],
        br[class=em_hide] {
          display: none !important;
        }
        img[class=em_full_img] {
          width: 100% !important;
          height: auto !important;
          max-width: 100% !important;
        }
        td[class=em_align_cent] {
          text-align: center !important;
        }
        td[class=fix_h] {
          height: 25px !important;
        }
        td[class=em_txt1] {
          font-size: 24px !important;
          line-height: 32px !important;
        }
        td[class=em_txt2] {
          font-size: 18px !important;
          line-height: 22px !important;
        }
      }
      @media only screen and (max-width:480px) {
        *[class=showMobile] {
          display: block !important;
          height: auto !important;
          max-height: inherit !important;
          overflow: visible !important;
        }
        *[class=showMobile1] {
          display: inline !important;
          height: auto !important;
          max-height: inherit !important;
          overflow: visible !important;
        }
        *[class=noMobile] {
          display: none !important;
          overflow: hidden !important;
          height: 0px !important;
        }
        table[class=em_wrapper] {
          width: 100% !important;
        }
        td[class=em_aside] {
          padding-left: 10px !important;
          padding-right: 10px !important;
        }
        td[class=em_hide],
        table[class=em_hide],
        span[class=em_hide],
        br[class=em_hide] {
          display: none !important;
        }
        img[class=em_full_img] {
          width: 100% !important;
          height: auto !important;
          max-width: 100% !important;
        }
        td[class=em_align_cent] {
          text-align: center !important;
        }
        td[class=fix_h] {
          height: 25px !important;
        }
        td[class=em_txt1] {
          font-size: 24px !important;
          line-height: 32px !important;
        }
        td[class=em_txt2] {
          font-size: 18px !important;
          line-height: 22px !important;
        }
        span[class=em_txt3] {
          font-size: 18px !important;
          line-height: 22px !important;
        }
        *[class=em_text4] {
          font-size: 13px !important;
          letter-spacing: 0.02em;
          text-decoration: none;
        }
        *[class=em_text5] {
          font-size: 17px !important;
          letter-spacing: 0.03em;
        }
      }
    </style>
  </head>
  <body style="margin:0px; padding:0px;" bgcolor="#ffffff">

    <!--Full width table start-->
    <table width="100%" border="0" align="center" bgcolor="#ffffff" cellpadding="0" cellspacing="0">

      <!--  header -->
      <tr>
        <td align="center" bgcolor="#ffffff" class="em_aside">
          <table width="600" border="0" bgcolor="#ffffff" cellspacing="0" cellpadding="0" class="em_wrapper">
            <tr>
              <td align="left" valign="middle" style="font-family: Corbel, Helvetica, Verdana, sans-serif; font-size: 1px; color: #ffffff; text-align: left; line-height:1px;">
                <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
                  <tr>
                    <td class="stylingblock-content-wrapper camarker-inner">
                      <div style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden; font-family:Arial, Helvetica, sans-serif; font-size:11px; color:#999999;" align="center">Now, let's get you ready for bed.
                        &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
                        &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
                      </div>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!--BEGIN MAIN CONTENT-->
      <table width="600" border="0" class="em_wrapper" align="center" cellpadding="0" cellspacing="0" bgcolor="#ffffff">
        <tr>
          <td align="center">
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
              <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                  <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td align="center"><a href="https://casper.com/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" title="Let's Get Sleepy" data-linkto="https://"><img data-assetid="310147" src="http://image.mail.casper.com/lib/fe951372746d067d70/m/8/fe0a2fd2-c4ea-425a-a7a3-e54c51924236.gif" alt="Hello, dreamer. Welcome to Casper! Let's Get Sleepy" height="731" width="640" style="display: block; padding: 0px; text-align: center; height: 731px; width: 640px; border: 0px;"></a></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
              <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                  <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td align="center"><a href="https://casper.com/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" title="" data-linkto="https://"><img data-assetid="310010" src="http://image.mail.casper.com/lib/fe951372746d067d70/m/8/3959fb03-a9fe-4380-8622-8762cdd5bb0a.png" alt="Here's what you'll get" width="640" style="display: block; padding: 0px; text-align: center; height: auto; width: 100%; border: 0px;"></a></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
              <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                  <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td align="center">
                        <a href="https://casper.com/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" title="Latest Snooze" data-linkto="https://"><img data-assetid="310013" src="http://image.mail.casper.com/lib/fe951372746d067d70/m/8/19207678-8ba0-4a29-b34d-33acbe9d9101.png" alt="Latest Snooze. Be the first to know about our latest and dreamiest products." width="640" style="display: block; padding: 0px; text-align: center; height: auto; width: 100%; border: 0px;"></a></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
              <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                  <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td align="center">
                        <a href="https://casper.com/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" title="Early Access" data-linkto="https://"><img data-assetid="310007" src="http://image.mail.casper.com/lib/fe951372746d067d70/m/8/3e59b688-c012-4402-89f0-7cc4f9a29533.png" alt="Early Access. You'll get first dibs on our sales and special promotions. " width="640" style="display: block; padding: 0px; text-align: center; height: auto; width: 100%; border: 0px;"></a></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
              <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                  <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td align="center">
                        <a href="https://casper.com/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" title="Bedtime Reading" data-linkto="https://"><img data-assetid="310008" src="http://image.mail.casper.com/lib/fe951372746d067d70/m/8/2e045eaa-2145-4049-8027-746e78092880.png" alt="Bedtime Reading. Learn sleep tips and more with the Snoozeletter. " width="640" style="display: block; padding: 0px; text-align: center; height: auto; width: 100%; border: 0px;"></a></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
              <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                  <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td align="center">
                        <a href="https://casper.com/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" title="Free Shipping" data-linkto="https://"><img data-assetid="310011" src="http://image.mail.casper.com/lib/fe951372746d067d70/m/8/5e10bec6-d661-409a-9425-cdf25609f844.png" alt="Free Shipping. Enjoy fast, free delivery on every Casper order*. " width="640" style="display: block; padding: 0px; text-align: center; height: auto; width: 100%; border: 0px;"></a></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
              <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                  <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                      <td align="center">
                        <a href="https://casper.com/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" title="Sleep Tip #1" data-linkto="https://"><img data-assetid="310006" src="http://image.mail.casper.com/lib/fe951372746d067d70/m/8/2bd9c11a-0c87-46fe-b59c-a4285ef6ea36.png" alt="Sleep Tip #1. For restful zzz's, try to avoid caffeine after 12pm. " width="640" style="display: block; padding: 0px; text-align: center; height: auto; width: 100%; border: 0px;"></a></td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
              <tr>
                <td class="stylingblock-content-wrapper camarker-inner">
                  <table width="100%" align="center" cellpadding="0" cellspacing="0">

                    <!--<tr>     <td align="center" height="50" style="font-size: 20px; line-height: 32px; color: #ffffff; font-family: 'Calibre Light', 'Roboto', sans-serif !important; font-weight: 300; vertical-align: middle;"><strong>Still not sure? Check out this special offer.</strong>       </td>    </tr>-->
                    <tr>
                      <td align="center">
                        <a href="https://casper.com/bundles/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" target="_blank"><img src="http://image.mail.casper.com/lib/fe951372746d067d70/m/8/b9f1a02c-f3f6-42b2-99b2-494fa8f32278.jpg" alt="Shop bundles" alias="Shop bundles" style="display: block; border: 0;" width="640" height="279"></a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <!--END MAIN CONTENT-->

      <!--BEGIN SOCIAL-->
      <tr>
        <td>
          <table width="100%" align="center">
            <tr>
              <td align="center">
                <table width="600" border="0" cellspacing="0" cellpadding="0" class="em_wrapper" align="center">
                  <tr>
                    <td height="5" style="line-height:0px; font-size:0px;">&nbsp;</td>
                    <td height="20" style="line-height:0px; font-size:0px;">&nbsp;</td>
                  </tr>
                  <tr>
                    <td align="center">
                      <table border="0" align="center" cellpadding="0" cellspacing="0">
                        <tr>
                          <td><a href="https://www.instagram.com/accounts/login/?next=%2Fcasper%2F%3Fet_rid%3D707880931%26mi_u%3D707880931%26utm_campaign%3D2020_0326_Welcome_1_enUS%26utm_medium%3Demail%26utm_source%3DSFMC%26utm_term%3D707880931" target="_blank"> <img src="http://image.mail.casper.com/lib/fe951372746d067d70/m/3/Casper_Redesign_30.jpg" width="40" height="40" alt="Instagram" style="display:block;" border="0" /> </a></td>
                          <td width="10">&nbsp;</td>
                          <td><a href="https://www.facebook.com/Casper/?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" target="_blank"> <img src="http://image.mail.casper.com/lib/fe951372746d067d70/m/3/Casper_Redesign_32.jpg" width="40" height="40" alt="Facebook" style="display:block;" border="0" /> </a></td>
                          <td width="10">&nbsp;</td>
                          <td><a href="https://twitter.com/casper?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" target="_blank"> <img src="http://image.mail.casper.com/lib/fe951372746d067d70/m/3/Casper_Redesign_34.jpg" width="40" height="40" alt="Twitter" style="display:block;" border="0" /> </a></td>
                          <td width="10">&nbsp;</td>
                          <td><a href="https://www.pinterest.com/caspersleep?utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" target="_blank"> <img src="http://image.mail.casper.com/lib/fe951372746d067d70/m/3/Casper_Redesign_36.jpg" width="40" height="40" alt="Pinterest" style="display:block;" border="0" /> </a></td>
                          <td width="10">&nbsp;</td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td height="5" style="line-height:0px; font-size:0px;">&nbsp;</td>
                    <td height="20" style="line-height:0px; font-size:0px;">&nbsp;</td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>

          <!--END SOCIAL-->

          <!--BEGIN FOOTER-->
          <table width="100%" align="Center">
            <tr>
              <td align="center">
                <table width="600" border="0" cellspacing="0" cellpadding="0" class="em_wrapper" align="center" style="text-align: center; padding-left:5px; padding-right:5px;">
                  <tr>
                    <td width="600" class="em_text4" style="color:#b2b2b2;font-family:Arial, Helvetica, sans-serif;font-size:10px; text-align: center" align="center"><a href="#" style="text-decoration:none; color:#b2b2b2;font-family:Arial, Helvetica, sans-serif; text-align: center"><u>View in Browser</u></a>
                    </td>
                  </tr>
                  <tr>
                    <td height="20">&nbsp;</td>
                  </tr>
                  <tr>
                    <td width="600" class="em_text4" style="color:#b2b2b2;font-family:Arial, Helvetica, sans-serif;font-size:10px; font-weight:bold; letter-spacing: 0.02em; text-align: center" align="center"><a href="mailto:support@casper.com" style="color:#999999; text-decoration:none;">support@casper.com</a> | <a href="tel:888-995-2507" style="color:#999999; text-decoration:none;"> +1 888-995-2507</a></td>
                  </tr>
                  <tr>
                    <td height="14">&nbsp;</td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>

          <!--BEGIN DISCLAIMER-->
          <table width="600" border="0" class="em_wrapper" align="center" cellpadding="0" cellspacing="0" bgcolor="#ffffff">
            <tr>
              <td align="center">
                <table cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%; " class="stylingblock-content-wrapper">
                  <tr>
                    <td class="stylingblock-content-wrapper camarker-inner">
                      <table align="Center">
                        <tr>
                          <td style="color: #b2b2b2; font-family: Arial, Helvetica, sans-serif; font-size: 10px;" width="600" align="center">
                            <font face="Arial, Helvetica, sans-serif" color="b2b2b2">*Additional shipping charges may apply to Alaska and Hawaii. See
                              <a href="https://casper.com/terms/?j=3416962&sfmc_sub=707880931&l=57_HTML&u=234170957&mid=7219205&jb=159&utm_source=SFMC&utm_medium=email&et_rid=707880931&utm_term=707880931&utm_campaign=2020_0326_Welcome_1_enUS&&&&&mi_u=707880931" target="_blank" style="text-decoration-line: none; color: #b2b2b2 !important;">casper.com/terms/</a> for additional terms.<br><br>
                            </font>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>

          <!--END DISCLAIMER-->
          <table align="center" class="noMobile" style="font-size:0px; line-height:0px;">
            <tr>
              <div class="noMobile">
                <td width="600" style="color:#b2b2b2;font-family:Arial, Helvetica, sans-serif;font-size:10px; line-height:15px; text-align: center; padding-left:5px; padding-right:5px; padding-bottom:30px;" class="noMobile" align="center"> 3 World Trade Center - Floor 39
                  New York, NY 10007 | &copy; 2020 Casper Sleep Inc.<br /> If you prefer not to receive emails, you may <a title="MyPage" href="#" style="color:#b2b2b2; text-decoration:underline;"> unsubscribe</a>. <a href="/privacy/?et_rid=707880931&mi_u=707880931&utm_campaign=2020_0326_Welcome_1_enUS&utm_medium=email&utm_source=SFMC&utm_term=707880931" style="text-decoration:none; color:#b2b2b2;font-family:Arial, Helvetica, sans-serif; text-align: center"><u>Casper Privacy Policy</u></a>
                </td>
              </div>
            </tr>
          </table>
          <div class="showMobile1" bgcolor="#ffffff" align="center">
            <table bgcolor="#ffffff" class="showMobile1" align="center" height="0" width="100%" cellspacing="0" cellpadding="0" border="0">
              <tr>
                <td class="showMobile1" align="center">
                  <table bgcolor="#ffffff" class="showMobile1" style="display: none; overflow: hidden; height: 0px; max-height: 0px;" align="center" width="100%" cellspacing="0" cellpadding="0" border="0">
                    <tr>
                      <td width="600" style="color:#b2b2b2;font-family:Arial, Helvetica, sans-serif;font-size:10px; line-height:20px; text-align: center; padding-left:5px; padding-right:5px; padding-bottom:20px;" class="em_text4" align="center"> 3 World Trade Center - Floor 39
                        New York, NY 10007 <br>
                        &copy; 2020 Casper Sleep Inc.<br /> If you prefer not to receive emails, you may <a title="MyPage" href="#" style="color:#b2b2b2; text-decoration:underline;"> unsubscribe</a>.<a href="/privacy/?et_rid=707880931&mi_u=707880931&utm_campaign=2020_0326_Welcome_1_enUS&utm_medium=email&utm_source=SFMC&utm_term=707880931" style="color:#b2b2b2; text-decoration:underline;"><u>Casper Privacy Policy</u></a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </div>
        </td>
      </tr>
    </table>
  </body>
</html>"""