VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Form_’›Õ… «·œŒÊ·"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Compare Database


Private Sub Form_Current()
DoCmd.ShowToolbar "ribbon", acToolbarNo
End Sub

Private Sub Form_Load()
DoCmd.ShowToolbar "ribbon", acToolbarNo
End Sub

Private Sub  ›’Ì·_Click()

End Sub

Private Sub œŒÊ·_Click()
Dim userlevel As String
If Nz(DLookup("password", "user", "username = '" & Me.txtusername & "'"), "password") = Me.txtpassword Then
userlevel = Nz(DLookup("seclevel", "user", "username = '" & Me.txtusername & "'"))
If userlevel = "Admin" Then
DoCmd.Close
DoCmd.OpenForm "Mainpage"

ElseIf userlevel = "user" Then
DoCmd.Close
DoCmd.OpenForm "mainpage"
Form_Mainpage.COME.Enabled = False
Form_Mainpage.BACK.Enabled = False
End If
Else
MsgBox "Sorry .... Wrong Username or Password", vbExclamation, "ACCESS Denied"
End If
End Sub
