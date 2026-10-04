# ComfyUI Notifications

Custom node para exibir uma notificação do Windows e tocar o som do sistema
durante a execução de um workflow no ComfyUI. O node `Windows Notification`
permite definir o título e a descrição do aviso.

## Instalação

Coloque esta pasta em `ComfyUI/custom_nodes/ComfyUI-Notifications` e reinicie o
ComfyUI. Se o ComfyUI já estiver aberto, reinicie-o depois de adicionar ou
atualizar o node para que ele seja carregado.

## Uso

Adicione `Windows Notification` ao workflow, conecte qualquer saída ao socket
`value` e personalize `title` e `description`. O node exibe a notificação e
toca o som Asterisk do sistema. A saída `value` é o mesmo objeto recebido,
sem conversão, para que o workflow possa continuar. Por exemplo, conecte uma
imagem à entrada e use a saída para alimentar `Save Image`.

## Requisitos

- Windows com as notificações e os sons do sistema habilitados.
- ComfyUI.
- Windows PowerShell (`powershell.exe`), incluído no Windows.

O node não precisa de dependências Python adicionais. O aviso pode ser
suprimido pelas configurações de notificação ou pelo modo Não incomodar do
Windows.
