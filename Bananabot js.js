var botActive = true; // Variable to track the bot's active state

Events.on(EventType.PlayerChatEvent, event => {
    var messageText = event.message.trim();
    var player = event.player;

    // Debugging message to see the command received
    Call.sendChatMessage("[debug] Received message: " + messageText);

    // Command to toggle the bot on and off
    if (messageText === "#fishbot on") {
        botActive = true;
        Call.sendChatMessage("[gold]Fishbot is now [green]ON[gold].");
    } else if (messageText === "#fishbot off") {
        botActive = false;
        Call.sendChatMessage("[gold]Fishbot is now [red]OFF[gold].");
    }

    // If the bot is active, respond to "hey fishbot"
    if (botActive && messageText.startsWith("hey fishbot")) {
        Call.sendChatMessage("hello, I am fishbot");
    }
});

Events.on(EventType.PlayerJoin, event => {
    if (botActive) { // Only send the welcome message if the bot is active
        var player = event.player;
        var playerName = player.name;
        Call.sendChatMessage("[gold]Hello [white]" + playerName + "!");
    }
});
