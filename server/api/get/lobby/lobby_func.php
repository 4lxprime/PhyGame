<?php

function get_shop() {
    $r=array (
      'daily1' => 
      array (
        'itemGrants' => 
        array (
          0 => 'AthenaCharacter:CID_021_Athena_Commando_F',
        ),
        'price' => 1200,
      ),
      'daily2' => 
      array (
        'itemGrants' => 
        array (
          0 => 'AthenaGlider:Glider_Prismatic',
        ),
        'price' => 800,
      ),
      'daily3' => 
      array (
        'itemGrants' => 
        array (
          0 => 'AthenaPickaxe:HalloweenScythe',
        ),
        'price' => 2500,
      ),
      'daily4' => 
      array (
        'itemGrants' => 
        array (
          0 => 'AthenaCharacter:CID_024_Athena_Commando_F',
        ),
        'price' => 1200,
      ),
      'daily5' => 
      array (
        'itemGrants' => 
        array (
          0 => 'AthenaPickaxe:BoltonPickaxe',
        ),
        'price' => 800,
      ),
      'daily6' => 
      array (
        'itemGrants' => 
        array (
          0 => 'AthenaCharacter:CID_022_Athena_Commando_F',
        ),
        'price' => 1200,
      ),
      'featured1' => 
      array (
        'itemGrants' => 
        array (
          0 => 'AthenaCharacter:CID_030_Athena_Commando_M_Halloween',
        ),
        'price' => 1500,
      ),
      'featured2' => 
      array (
        'itemGrants' => 
        array (
          0 => 'AthenaCharacter:CID_029_Athena_Commando_F_Halloween',
        ),
        'price' => 1200,
      ),
    );
    echo json_encode($r);

}

function get_loginmess() {
    $r=array(
        '_title' => 'Fortnite Game',
        '_activeDate' => '2017-08-30T03:20:48.050Z',
        'lastModified' => '2019-11-01T17:33:35.346Z',
        '_locale' => 'en-US',
        'loginmessage' => 
        array (
          '_title' => 'LoginMessage',
          'loginmessage' => 
          array (
            '_type' => 'CommonUI Simple Message',
            'message' => 
            array (
              '_type' => 'CommonUI Simple Message Base',
              'title' => 'Project Nocturno | Saison 1',
              'body' => 'Bienvenue sur le Project Nocturno !
      Le discord: https://discord.gg/GrrB3s5CXC 
      Notre TikTok: @project.nocturno
      Si vous avez des problème de casier, merci de faire un ticket.
      Credit à Lawin pour le lobby !',
            ),
          ),
        ),
      );

      echo json_encode($r);
}

function get_emergency() {
    $r=array (
        'emergencynotice' => 
        array (
          'news' => 
          array (
            '_type' => 'Battle Royale News',
            'messages' => 
            array (
              0 => 
              array (
                'hidden' => true,
                '_type' => 'CommonUI Simple Message Base',
                'title' => 'Project Nocturno',
                'body' => 'Maintenance prévue à 20h jusqu\'à 10h.
      Pour en savoir plus tout est sur le serveur discord.',
                'spotlight' => true,
              ),
            ),
          ),
        ),
    );

    echo json_encode($r);

}

function get_news() {
    $r=array (
        'battleroyalenews' => 
        array (
          'news' => 
          array (
            '_type' => 'Battle Royale News',
            'motds' => 
            array (
              0 => 
              array (
                'entryType' => 'Website',
                'image' => 'https://fortnite-public-service-prod11.ol.epicgames.com/images/motd.png',
                'tileImage' => 'https://fortnite-public-service-prod11.ol.epicgames.com/images/motd-s.png',
                'videoMute' => false,
                'hidden' => false,
                'tabTitleOverride' => 'LawinServer',
                '_type' => 'CommonUI Simple Message MOTD',
                'title' => 
                array (
                  'ar' => 'مرحبًا بك في LawinServer!',
                  'en' => 'Welcome to LawinServer!',
                  'de' => 'Willkommen bei LawinServer!',
                  'es' => '¡Bienvenidos a LawinServer!',
                  'es-419' => '¡Bienvenidos a LawinServer!',
                  'fr' => 'Bienvenue sur LawinServer !',
                  'it' => 'Benvenuto in LawinServer!',
                  'ja' => 'LawinServerへようこそ！',
                  'ko' => 'LawinServer에 오신 것을 환영합니다!',
                  'pl' => 'Witaj w LawinServerze!',
                  'pt-BR' => 'Bem-vindo ao LawinServer!',
                  'ru' => 'Добро пожаловать в LawinServer!',
                  'tr' => 'LavinServer\'a Hoş Geldiniz!',
                ),
                'body' => 
                array (
                  'ar' => 'استمتع بتجربة لعب استثنائية!',
                  'en' => 'Have a phenomenal gaming experience!',
                  'de' => 'Wünsche allen ein wunderbares Spielerlebnis!',
                  'es' => '¡Que disfrutes de tu experiencia de videojuegos!',
                  'es-419' => '¡Ten una experiencia de juego espectacular!',
                  'fr' => 'Un bon jeu à toutes et à tous !',
                  'it' => 'Ti auguriamo un\'esperienza di gioco fenomenale!',
                  'ja' => '驚きの体験をしよう！',
                  'ko' => '게임에서 환상적인 경험을 해보세요!',
                  'pl' => 'Życzymy fenomenalnej gry!',
                  'pt-BR' => 'Tenha uma experiência de jogo fenomenal!',
                  'ru' => 'Желаю невероятно приятной игры!',
                  'tr' => 'Muhteşem bir oyun deneyimi yaşamanı dileriz!',
                ),
                'offerAction' => 'ShowOfferDetails',
                'videoLoop' => false,
                'videoStreamingEnabled' => false,
                'sortingPriority' => 90,
                'websiteButtonText' => 'Discord',
                'websiteURL' => 'https://discord.gg/KJ8UaHZ',
                'id' => '61fb3dd8-f23d-45cc-9058-058ab223ba5c',
                'videoAutoplay' => false,
                'videoFullscreen' => false,
                'spotlight' => false,
              ),
            ),
            'messages' => 
            array (
              0 => 
              array (
                'image' => 'https://cdn.discordapp.com/attachments/735984479906037845/1018900749889064980/nocturno.jpg',
                'hidden' => false,
                '_type' => 'CommonUI Simple Message Base',
                'adspace' => 'PROJECT NOCTURNO',
                'title' => 'Bienvenue sur le Project Nocturno !',
                'body' => 'Voici la saison 1 entièrement fonctionnel',
                'spotlight' => true,
              ),
              1 => 
              array (
                'image' => 'https://cdn.discordapp.com/attachments/735984479906037845/1018900832416170004/fortnite.png',
                'hidden' => false,
                '_type' => 'CommonUI Simple Message Base',
                'adspace' => 'BIENVENUE',
                'title' => 'Starter Pack',
                'body' => 'Vous commencez avec tous 500 V-Bucks !
      A chaque top 1 = 1000 V-Bucks
      Si vous avez des problèmes, merci de faire un ticket sur notre discord.',
                'spotlight' => true,
              ),
            ),
          ),
          '_title' => 'battleroyalenews',
          'header' => '',
          'style' => 'SpecialEvent',
          '_noIndex' => false,
          'alwaysShow' => false,
          '_activeDate' => '2018-08-17T16:00:00.000Z',
          'lastModified' => '2019-10-31T20:29:39.334Z',
          '_locale' => 'en-US',
        ),
    );

    echo json_encode($r);
    
}

?>