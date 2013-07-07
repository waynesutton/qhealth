<?php

/******************************************************************
 * Requirements
 ******************************************************************/
require_once 'libraries/swift/lib/swift_required.php';

/******************************************************************
 * Constants
 ******************************************************************/
define('MESSAGE_SUBJECT', 'QHealth - Contact Message');
define('MESSAGE_FROM_EMAIL', 'contact@qhealth.org');
define('MESSAGE_FROM_NAME', 'QHealth');
define('MESSAGE_TO_EMAIL', 'contact@qhealth.org');

define('TRANSPORT_SERVER', 'smtp.qhealth.org');
define('TRANSPORT_PORT', 26);
define('TRANSPORT_USERNAME', 'contact@qhealth.org');
define('TRANSPORT_PASSWORD', 'sqmail13health');

/******************************************************************
 * Configure transport
 ******************************************************************/
$transport = Swift_SmtpTransport::newInstance(TRANSPORT_SERVER, TRANSPORT_PORT)
    ->setUsername(TRANSPORT_USERNAME)
    ->setPassword(TRANSPORT_PASSWORD);
$mailer = Swift_Mailer::newInstance($transport);

/******************************************************************
 * Send email
 ******************************************************************/
if (!empty($_POST['email']) && !empty($_POST['name']) && !empty($_POST['message'])) {
    $body = sprintf("Email: %s \nName: %s\nBody: %s", $_POST['email'], $_POST['name'], $_POST['message']);

    $message = Swift_Message::newInstance()
        ->setSubject(MESSAGE_SUBJECT)
        ->setFrom(array(MESSAGE_FROM_EMAIL => MESSAGE_FROM_NAME))
        ->setTo(array(MESSAGE_TO_EMAIL))
        ->setBody($body);

    $mailer->send($message);
}